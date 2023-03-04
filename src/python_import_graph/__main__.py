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

"""src/python_import_graph/__main__.py:

Python import graph.

"""

__author__ = "Dietrich Bollmann"
__email__ = "dietrich@newskylabs.net"
__copyright__ = "Copyright 2023 Dietrich Bollmann"
__url__ = "https://github.com/glottai/glottai-cedict"
__license__ = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__ = "2023/02/26"

import click

from python_import_graph.parser import calculate_import_graph

from python_import_graph.printer import (
    print_in_graphviz_dot_format,
    print_as_indented_list,
)


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--dot", is_flag=True, help="Print graph in graphviz dot format."
)
def main(filename, dot):
    """Show the local import graph given a Python source file and directory."""

    import_graph = calculate_import_graph(filename)

    if dot:
        print_in_graphviz_dot_format(import_graph)

    else:
        print_as_indented_list(import_graph)


if __name__ == "__main__":
    main()
