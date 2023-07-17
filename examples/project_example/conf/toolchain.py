"""
===========================================
Toolchain configuration for example project
===========================================

:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: July 2023
"""

from pathlib                import Path

from uninja.toolchain.base  import Toolchain
from uninja.toolchain.c.gcc import ToolchainGCC

from uninja.codebase        import c as c_code

import conf.dirs

import dataclasses


################################
# Toolchain declaration
################################

class CustomToolchain(ToolchainGCC):
    def __init__(self):
        super().__init__(
            cflags = (
                "-Wall",
                "-Werror",
                "-pedantic"
            )
        )

    def process_source(self, tools: Toolchain, src: c_code.Source):
        # Add filename in defines
        src = dataclasses.replace(src, defines = src.defines.union(frozenset({
            c_code.Define(name="FILENAME", value=src.path.name)
        })))

        return super().process_source(tools, src)


gcc = CustomToolchain()

tools = Toolchain(root_dir=conf.dirs.project_dir, build_dir=conf.dirs.build_dir)
gcc.associate_to(tools)