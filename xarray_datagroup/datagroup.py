from __future__ import annotations

import typing as T

import xarray as xr

from . import store

# Differences with xr.Dataset:
# - no dims, DataArrays may have incompatible dimensions
# - coords are the Coordinate variables contained in the path, DataArrays may have coordinates contained
#   in other groups
class DataGroup:
    attrs: T.MutableMapping[T.Hashable, T.Any]
    data_vars: T.MutableMapping[T.Hashable, xr.DataArray]
    coords: T.MutableMapping[T.Hashable, xr.DataArray]

    parent: DataGroup | None
    groups: T.MutableMapping[T.Hashable, DataGroup]

    path: store.StorePath

    def tree(self) -> str:
        ...

    def get(self, item) -> T.Union[DataGroup, xr.DataArray]:
        ...
