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

"""src/parser.py:

Python import graph parser.

"""

import sys
import ast

from python_import_graph.finder import find_imported_file


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

        imported_files = process_body(directory, p, [])

        return imported_files

    return None


def process_body(directory, e, imported_files):
    imported_files = process_elements(directory, e.body, imported_files)

    return imported_files


def process_elements(directory, elts, imported_files):
    for e in elts:
        imported_files = process_element(directory, e, imported_files)

    return imported_files


def process_element(directory, e, imported_files):
    # DEBUG
    # | print(ast.dump(e, indent=4))

    if isinstance(e, ast.Import):
        return get_imported_files_from_Import(e, imported_files)

    elif isinstance(e, ast.ImportFrom):
        return get_imported_files_from_ImportFrom(directory, e, imported_files)

    elif hasattr(e, "body"):
        return process_body(directory, e, imported_files)

    else:
        return imported_files


def get_imported_files_from_Import(import_statement, imported_files):
    # DEBUG
    # | print(ast.dump(import_statement, indent=4))

    names = import_statement.names

    for name in names:
        name = name.name

        filename = find_imported_file(name)

        if filename is not None and filename not in imported_files:
            imported_files.append(filename)

    return imported_files


def get_imported_files_from_ImportFrom(
    directory, import_statement, imported_files
):
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

    for name in names:
        name = name.name

        filename = find_imported_file(name, module=module)

        # DEBUG
        # | print(
        # |     f'DEBUG find_imported_file("{name}", module="{module}")'
        # |     f' => "{filename}"'
        # | )

        if filename is not None and filename not in imported_files:
            imported_files.append(filename)

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
