# xarray-datagroup

Assumptions:

- zarr/h5py hierarchical store with groups, datasets/arrays and attributes
- CF definitions of hierarchically defined data and coordinate variables

Data is represented as `DataGroup`s and `xr.DataArray`s, so the `DataGroup` class
serves the same function as `xr.Dataset` and supersedes it.
