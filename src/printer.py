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

"""src/printer.py:

Functionality to print Python import graph.

"""


def print_as_indented_list(import_graph):
    for filename, filenames in import_graph.items():
        print(f"  {filename}")

        for filename in filenames:
            print(f"    {filename}")

        print("")


def print_in_graphviz_dot_format(import_graph):
    print("digraph {")
    for filename, filenames in import_graph.items():
        print(f'  "{filename}" -> {{')

        for filename in filenames:
            print(f'    "{filename}"')

        print("  }")

    print("}")
