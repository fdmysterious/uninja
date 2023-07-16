import sys
import uninja
import logging
import datetime

from uninja.codebase.c.source     import Source, SourceLang
from uninja.codebase.c.component  import Component
from uninja.codebase.c.executable import Executable

from uninja.rule                  import Rule, Phony
from uninja.target                import Target, TargetVar, TargetVars

from uninja.toolchain.base        import Toolchain
from uninja.toolchain.c.gcc       import ToolchainGCC

from uninja.utils                 import color_log

from pathlib                      import Path

from pprint    import pprint
from functools import reduce

color_log.install(level=logging.INFO)

######################################
# Toolchain init.
######################################

gcc = ToolchainGCC(
    cflags = (
        "-Wall",
        "-Werror",
        "-pedantic"
    )
)

tools = Toolchain(root_dir=Path.cwd(), build_dir=Path("build").resolve())
gcc.associate_to(tools)


######################################
# Components definition
######################################

bar_component = Component(
    name = "bar",
    path = Path("src/bar"),

    srcs = frozenset({
        Source(path = Path("bar.c"), lang=SourceLang.C)
    })
)

foo_component = Component(
    name = "foo",
    path = Path("src/foo"),

    srcs = frozenset({
        Source(path = Path("foo.c"), lang=SourceLang.C)
    }),

    components_dependencies = frozenset({bar_component})
)

main_component = Component(
    name = "main",
    path = Path("src/main"),

    srcs = frozenset({
        Source(path = Path("main.c"), lang=SourceLang.C)
    }),

    components_dependencies = frozenset({
        foo_component,
        bar_component
    })
)

main_app = Executable(
    "bin/main",

    components = frozenset({
        main_component
    })
)


targets_gcc   = tools.process(main_app)

# Phony build target
targets_build = Target(
    name = "build",
    rule = Phony(),
    deps = targets_gcc
)

tools.build_dir.mkdir(exist_ok=True)
with open(f"{tools.build_dir}/build.ninja", "w") as fhandle:
    uninja.output(fhandle, (targets_build,))