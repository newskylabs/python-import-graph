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

"""src/finder.py:

Python import file finder.

"""

import os.path


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
