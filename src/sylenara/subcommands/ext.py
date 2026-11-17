import os
import sys
from argparse import Namespace

from sylenara.utils.shell_tools import shell_script


class Command:
    args: Namespace

    def __init__(self, args: Namespace) -> None:
        self.args = args

    def run(self) -> None:
        # The tool does the work (list | info | inspect | install <zip> | remove <id> [--purge] | enable | disable | rescan,
        # or <id> [<command> [args]]: the commands an extension offers)
        tool = shell_script("ext.py", env="SYLENARA_EXT_TOOL")
        os.execv(sys.executable, [sys.executable, tool, *self.args.ext_args])
