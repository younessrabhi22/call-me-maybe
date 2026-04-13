import os
from pathlib import Path


def print_tree(dir_path: Path, prefix: str = ""):
    # Get all files and folders, but ignore hidden ones like .git or __pycache__
    contents = sorted(
        [
            p
            for p in dir_path.iterdir()
            if not p.name.startswith(".") and p.name != "__pycache__"
        ]
    )

    # Create the branch lines
    pointers = ["├── "] * (len(contents) - 1) + ["└── "]

    for pointer, path in zip(pointers, contents):
        print(prefix + pointer + path.name)
        if path.is_dir():
            extension = "│   " if pointer == "├── " else "    "
            print_tree(path, prefix=prefix + extension)


print(".")
print_tree(Path("."))
