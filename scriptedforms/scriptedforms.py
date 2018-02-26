# Scripted Forms -- Making GUIs easy for everyone on your team.
# Copyright (C) 2017 Simon Biggs

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version (the "AGPL-3.0+").

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License and the additional terms for more
# details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# ADDITIONAL TERMS are also included as allowed by Section 7 of the GNU
# Affrero General Public License. These aditional terms are Sections 1, 5,
# 6, 7, 8, and 9 from the Apache License, Version 2.0 (the "Apache-2.0")
# where all references to the definition "License" are instead defined to
# mean the AGPL-3.0+.

# You should have received a copy of the Apache-2.0 along with this
# program. If not, see <http://www.apache.org/licenses/LICENSE-2.0>.


import sys
import os
import argparse

from notebook.notebookapp import NotebookApp

from ._api_handlers import get_api_handlers
from ._scriptedforms_handlers import get_scriptedforms_handlers
from ._install_jupyter_server_extension import install_jupyter_server_extension


def load_jupyter_server_extension(notebook_app):
    api_handlers = get_api_handlers(
        notebook_app.port, notebook_app.notebook_dir)
    scriptedforms_handlers = get_scriptedforms_handlers()

    handlers = api_handlers + scriptedforms_handlers

    web_app = notebook_app.web_app
    web_app.add_handlers('.*$', handlers)


def load(filepath):
    install_jupyter_server_extension()

    absolute_path = os.path.abspath(filepath)
    if not os.path.exists(absolute_path):
        raise ValueError('file does not exist')

    directory, filename = os.path.split(absolute_path)

    # workaround for Notebook app using sys.argv
    sys.argv = [sys.argv[0]]
    NotebookApp.launch_instance(
        notebook_dir=directory,
        default_url='/scriptedforms/{}'.format(filename))


def main():
    parser = argparse.ArgumentParser(description='ScriptedForms.')
    parser.add_argument(
        'filepath', help='The file path of the form to open.')

    args = parser.parse_args()
    load(args.filepath, args)


if __name__ == '__main__':
    main()
