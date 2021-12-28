from __future__ import annotations

import typing as T

import xarray as xr


class Group(T.Protocol):
    attrs: T.MutableMapping[str, T.Any]
    encodings: T.MutableMapping[str, T.Any]


StorePath = str
Store = T.MutableMapping[StorePath, T.Union[Group, xr.Variable]]
