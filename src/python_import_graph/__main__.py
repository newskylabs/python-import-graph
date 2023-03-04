#!/usr/bin/env python
# ==========================================================
# Copyright 2023 Dietrich Bollmann
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------

"""src/python_import_graph.py

Python import graph.

"""

__author__ = "Dietrich Bollmann"
__email__ = "dietrich@newskylabs.net"
__copyright__ = "Copyright 2023 Dietrich Bollmann"
__url__ = "https://github.com/glottai/glottai-cedict"
__license__ = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__ = "2023/02/26"

import sys
import os.path
import click
import ast


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--dot", is_flag=True, help="Print graph in graphviz dot format."
)
def main(filename, dot):
    """Show the local import graph given a Python source file and directory."""

    import_graph = calculate_import_graph(filename)

    if dot:
        print("digraph {")
        for filename, filenames in import_graph.items():
            print(f'  "{filename}" -> {{')

            for filename in filenames:
                print(f'    "{filename}"')

            print("  }")

        print("}")

        sys.exit(0)

    print("")
    print("Import graph:")
    print("")
    for filename, filenames in import_graph.items():
        print(f"  {filename}:")

        for filename in filenames:
            print(f"    {filename}")

        print("")


def calculate_import_graph(filename):
    import_graph = {}

    calculate_import_graph_recursive(filename, import_graph)

    return import_graph


def calculate_import_graph_recursive(filename, import_graph):
    if filename in import_graph:
        return

    else:
        imported_files = get_imported_files(filename)

        import_graph[filename] = imported_files

        for filename in imported_files:
            calculate_import_graph_recursive(filename, import_graph)


def get_imported_files(filename):
    directory = filename.removesuffix(".py").split("/")

    with open(filename) as f:
        source = f.read()

        p = ast.parse(source, filename=filename, mode="exec")

        imported_files = process_body(directory, p)

        return imported_files

    return None


def process_body(directory, e):
    imported_files = process_elements(directory, e.body)

    return imported_files


def process_elements(directory, elts):
    imported_files = set()

    for e in elts:
        imported_files2 = process_element(directory, e)

        if imported_files2 is not None:
            imported_files = imported_files.union(imported_files2)

    return imported_files


def process_element(directory, e):
    if isinstance(e, ast.Import):
        # DEBUG
        # print(ast.dump(e, indent=4))

        return get_imported_files_from_Import(e)

    elif isinstance(e, ast.ImportFrom):
        # DEBUG
        # print(ast.dump(e, indent=4))

        return get_imported_files_from_ImportFrom(directory, e)

    elif hasattr(e, "body"):
        # DEBUG
        # print(ast.dump(e, indent=4))

        return process_body(directory, e)


def get_imported_files_from_Import(import_statement):
    # DEBUG
    # | print(ast.dump(import_statement, indent=4))

    names = import_statement.names

    imported_files = set()
    for name in names:
        name = name.name

        filename = find_imported_file(name)

        if filename is not None:
            imported_files.add(filename)

    return imported_files


def get_imported_files_from_ImportFrom(directory, import_statement):
    # DEBUG
    # | print(ast.dump(import_statement, indent=4))

    module = import_statement.module
    names = import_statement.names
    level = import_statement.level

    # Deal with relative module names
    module = resolve_relative_module(directory, level, module)

    # Import level undefined
    if module is None:
        print(f"ERROR Undefined import level: {level}")
        print("")
        print(ast.dump(import_statement, indent=4))
        print("")
        sys.exit(1)

    imported_files = set()
    for name in names:
        name = name.name

        filename = find_imported_file(name, module=module)

        # DEBUG
        # | print(
        # |     f'DEBUG find_imported_file("{name}", module="{module}")'
        # |     f' => "{filename}"'
        # | )

        if filename is not None:
            imported_files.add(filename)

    return imported_files


def resolve_relative_module(directory, level, module):
    ldir = len(directory)

    if level == 0:
        return module

    elif level < ldir:
        module = ".".join(directory[:-level]) + "." + module
        return module

    elif level == ldir:
        return module

    else:
        # Import level too high
        # for the given directory
        return None


def find_imported_file(name, module=None):
    """Get the longest filename corresponding to the given module and name."""

    if module is not None:
        # Example:
        # module:   "foo.bar.baz"
        # name:     "boo"
        # => path:  ["foo", "bar", "baz", "boo"]
        path = module.split(".")
        path.append(name)

    else:
        # Example:
        # name:     "one.two.three"
        # => path:  ["one", "two", "three"]
        path = name.split(".")

    # Get existing file
    # Return filename of existing file
    # corresponding to the longest existing subpath
    lpath = len(path)
    for i in range(lpath):
        subpath = path[: lpath - i]

        dirname = "/".join(subpath)

        # Does a file with the given filename exist?
        filename = dirname + ".py"
        if os.path.isfile(filename):
            # When a file with this name exists
            # return the filename
            return filename

        # Does a dir with the given dirname exist?
        elif os.path.isdir(dirname):
            filename = dirname + "/__init__.py"
            if os.path.isfile(filename):
                # When a file with this name exists
                # return the filename
                return filename

    # No file for the given module / name combination found
    return None


if __name__ == "__main__":
    main()
