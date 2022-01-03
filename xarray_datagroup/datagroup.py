from __future__ import annotations

import typing as T

import xarray as xr


# Differences with xr.Dataset:
# - no dims, DataArrays may have incompatible dimensions
# - coords are the Coordinate variables contained in the path, DataArrays may have coordinates contained
#   in other groups
class DataGroup:
    # from xr.Dataset
    attrs: T.MutableMapping[T.Hashable, T.Any]
    data_vars: T.MutableMapping[T.Hashable, xr.DataArray]
    coords: T.MutableMapping[T.Hashable, xr.DataArray]

    # tree navigation
    groups: T.MutableMapping[T.Hashable, DataGroup]

    def __init__(
        self,
        attrs: T.MutableMapping[T.Hashable, T.Any] | None = None,
        data_vars: T.MutableMapping[T.Hashable, xr.DataArray] | None = None,
        coords: T.MutableMapping[T.Hashable, xr.DataArray] | None = None,
        groups: T.MutableMapping[T.Hashable, DataGroup] | None = None,
    ) -> None:
        self.attrs = attrs or {}
        self.data_vars = data_vars or {}
        self.coords = coords or {}
        self.groups = groups or {}

    def tree(self) -> str:
        ...

    def get(self, item: str) -> T.Union[DataGroup, xr.DataArray]:
        current: T.Union[DataGroup, xr.DataArray] = self
        for name in item.split("/"):
            if not isinstance(current, DataGroup):
                raise KeyError(f"{item!r} not found {type(item)}")
            if name in current.groups:
                current = current.groups[name]
            elif name in current.data_vars:
                current = current.data_vars[name]
            elif name in current.coords:
                current = current.coords[name]
            else:
                raise KeyError(f"{item!r} not found")
        return current
