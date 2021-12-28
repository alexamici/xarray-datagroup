import typing as T

import xarray as xr


class DataTree(T.Mapping[str, T.Union["DataTree", xr.Variable]]):
    attrs: T.Mapping[str, T.Any]


class DataTreeDictProxy(dict, DataTree):
    attrs: T.Dict[str, T.Any]

    def __init__(self, *args, **kwargs):
        self.attrs = {}
        members = {}
        for key, value in dict(*args, **kwargs).items():
            if isinstance(value, xr.Variable):
                members[key] = value
            elif isinstance(value, dict):
                members[key] = DataTreeDictProxy(value)
            else:
                self.attrs[key] = value
        super().__init__(members)


def print_datatree(datatree: DataTree, name="/", prefix="") -> None:
    if prefix == "":
        print(f"{name}")

    variables = {}
    groups = {}
    for name, value in datatree.items():
        if isinstance(value, DataTree):
            groups[name] = value
        elif isinstance(value, xr.Variable):
            variables[name] = value
        else:
            raise ValueError(f"unexpected data type {type(value)}")

    if datatree.attrs:
        print(f"{prefix}├─ Attributes:")
    for name, value in datatree.attrs.items():
        print(f"{prefix}│      {name}: {value}")

    for name, value in variables.items():
        value_lines = str(value).splitlines()
        print(f"{prefix}├─ {name}: {value_lines[0]}")
        for line in value_lines[1:]:
            print(f"{prefix}│        {line}")

    for name, value in groups.items():
        print(f"{prefix}├─ {name}")
        print_datatree(value, name, prefix=prefix + "│  ")
