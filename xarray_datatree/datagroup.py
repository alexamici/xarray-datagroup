from __future__ import annotations

import typing as T

import xarray as xr

from . import store

# Differences with xr.Dataset:
# - no dims, DataArrays may have incompatible dimensions
# - coords are the Coordinate variables contained in the path, DataArrays may have coordinates contained
#   in other groups
class DataGroup(T.Protocol):
    attrs: T.MutableMapping[T.Hashable, T.Any]
    groups: T.MutableMapping[T.Hashable, DataGroup]
    data_vars: T.MutableMapping[T.Hashable, xr.DataArray]
    data_coords: T.Mapping[T.Hashable, xr.DataArray]

    parent: DataGroup
    path: store.StorePath
