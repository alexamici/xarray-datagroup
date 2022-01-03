# xarray-datagroup

Assumptions:

- zarr/h5py hierarchical store with groups, datasets/arrays and attributes
- CF definitions of hierarchically defined data and coordinate variables

Data is represented as `DataGroup`s and `xr.DataArray`s, so the `DataGroup` class
serves the same function as `xr.Dataset` and supersedes it.

`xr.Variable`s needs an additional `path` attribute.


## Usage

```python-repl
>>> import xarray_datagroup
>>> dg = xarray_datagroup("tree-data.nc")
>>> dg.tree()
/ - DataGroup
├── data_1 - DataArray {time: 10, lat: 16, lon: 32} float64
├── data_2 - DataArray {time: 10, lat: 16, lon: 32} float64
├── metadata - DataGroup
│   ├─ quality_flag - DataArray {lat: 2, lon: 4} int8
│   ├─ standard_error_1 - DataArray {/time: 10, /lat: 16, /lon: 32} float64
│   └─ standard_error_2 - DataArray {/time: 10, /lat: 16, /lon: 32} float64
└── overviews - DataGroup
    ├── x2 - DataGroup
    │   ├── data_1 - DataArray {/time: 10, lat: 8, lon: 16} float64
    │   └── data_2 - DataArray {/time: 10, lat: 8, lon: 16} float64
    └── x4 - DataGroup
        ├── data_1 - DataArray {/time: 10, lat: 4, lon: 8} float64
        └── data_2 - DataArray {/time: 10, lat: 4, lon: 8} float64

>>> dg.tree(show_coods=True)
/ - DataGroup
├── time - DataArray {time: 10} float64
├── lat - DataArray {lat: 16} float64
├── lon - DataArray {lon: 32} float64
├── data_1 - DataArray {time: 10, lat: 16, lon: 32} float64
├── data_2 - DataArray {time: 10, lat: 16, lon: 32} float64
├── metadata - DataGroup
│   ├─ lat - DataArray {lat: 2} int8
│   ├─ lon - DataArray {lon: 4} int8
│   ├─ quality_flag - DataArray {lat: 2, lon: 4} int8
│   ├─ standard_error_1 - DataArray {/time: 10, /lat: 16, /lon: 32} float64
│   └─ standard_error_2 - DataArray {/time: 10, /lat: 16, /lon: 32} float64
└── overviews - DataGroup
    ├── x2 - DataGroup
    │   ├── lat - DataArray {lat: 8} float64
    │   ├── lon - DataArray {lon: 16} float64
    │   ├── data_1 - DataArray {/time: 10, lat: 8, lon: 16} float64
    │   └── data_2 - DataArray {/time: 10, lat: 8, lon: 16} float64
    └── x4 - DataGroup
        ├── lat - DataArray {lat: 4} float64
        ├── lon - DataArray {lon: 8} float64
        ├── data_1 - DataArray {/time: 10, lat: 4, lon: 8} float64
        └── data_2 - DataArray {/time: 10, lat: 4, lon: 8} float64

>>> dg.data_vars["data_1"]
<xarray.DataArray 'data_1' (time: 10, lat: 16, lon: 32)>
...

>>> dg.get("metadata/quality_flag")  # better name? `.traverse()`?
<xarray.DataArray 'quality_flag' (lat: 2, lon: 4)>
...

```

For a flat netCDF file with the data in the root group the `DataGroup` has the same structure as the
`xr.Dataset`:

```python-repl
>>> dg_flat = xarray_datagroup("flat-data.nc")
>>> dg_flat.tree(show_coods=True)
/ - DataGroup
├── time - DataArray {time: 10} float64
├── lat - DataArray {lat: 16} float64
├── lon - DataArray {lon: 32} float64
├── quality_flag_lat - DataArray {quality_flag_lat: 2} float64
├── quality_flag_lon - DataArray {quality_flag_lon: 4} float64
├── data_1 - DataArray {time: 10, lat: 16, lon: 32} float64
├── data_2 - DataArray {time: 10, lat: 16, lon: 32} float64
├── quality_flag - DataArray {quality_flag_lat: 2, quality_flag_lon: 4} int8
├── standard_error_1 - DataArray {time: 10, lat: 16, lon: 32} float64
└── standard_error_2 - DataArray {time: 10, lat: 16, lon: 32} float64

```

Main similarities are:

- `.data_vars`, `.coords` and `.attrs` attributes behave the same

Main differences are:

- additional `.groups` attribute for tree traversal
- no `dims` - `DataArray`'s in a `DataGroup` may have incompatible dimensions
- the `coords` mapping contains the coordinate variables defined in the `DataGroup`, 
  not the coordinates of the contained data variables -
  `DataArray`'s in a `DataGroup` may have incompatible coordinates with the same name,
  as long as they are defined in a different `DataGroup`
- a `DataArray` may reference coordinate, auxiliary and ancillary variables in any `DataGroup`s
