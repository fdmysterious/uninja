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

from uninja.utils                 import color_log

from pathlib                      import Path

from pprint    import pprint
from functools import reduce

color_log.install(level=logging.INFO)

######################################
# Toolchain rules
######################################

RULE_CTIDY = Rule(
    name        = "ctidy",
    command     = "clang-tidy --quiet --use-color -checks=*,-llvm* $in -- $incdirs && touch $out",
    description = "Checking $in file..."
)

RULE_TOUCH_AFTER = Rule(
    name        = "touch_after",
    command     = "touch $out",
    description = "Touching $out..."
)


RULE_CC = Rule(
    name        = "cc",
    description = "Building $in...",
    command     = "gcc -fdiagnostics-color=always -MMD -MF $out.d -Wall -Werror -pedantic -g $incdirs -c $in -o $out",
    depfile     = "$out.d"
)

RULE_LD = Rule(
    name        = "ld",
    description = "Linking $out",
    command     = "gcc -o $out $in ",
)

RULE_LIB = Rule(
    name         = "lib",
    description  = "Creating static lib $out",
    command      = "ar rcs $out $in"
)

######################################
# Check Toolchain processors
######################################

def check_process_source(tools: Toolchain, src: Source):
    tools.log.info (f"Add check for C source: {src.path}")
    tools.log.debug(f" -- Source lang: {src.lang}", )
    tools.log.debug(f" -- Local incdirs: {src.incdirs_local}", )
    tools.log.debug(f" -- System incdirs: {src.incdirs_system}", )

    target = Target(
        name = f"ctidy/{src.path.resolve()}.lock",
        rule = RULE_CTIDY,
        deps = (src.path.resolve(),),
        vars = TargetVars.from_args(
            incdirs = f"-iquote {src.path.parent.resolve()}" + "".join(map(lambda x: f" -iquote {x!s}", src.incdirs_local)) + "".join(map(lambda x: f" -I {x!s}", src.incdirs_system))
        )
    )

    return (target,)


def check_process_component(tools: Toolchain, comp: Component):
    tools.log.info(f"Add check for C component: {comp.name}"  )
    tools.log.debug(f" -- Component path:    {comp.path}")
    #tools.log.debug(f" -- Component sources: {[x.path for x in comp.srcs]}")


    targets_srcs       = tuple()
    targets_comp       = tuple()
    components_incdirs = set()

    # Process components dependencies
    for sub_comp in comp.components_dependencies:
        tools.log.info(f" --> Configure component dependency: {sub_comp.name}")
        components_incdirs.add(sub_comp.path.resolve())
        targets_comp += tools.process(sub_comp)
    components_incdirs = frozenset(components_incdirs)

    # Prepend component path to sources
    for src in comp.srcs:
        src_path_prepend = Source(
            path = comp.path / src.path,
            lang = src.lang,

            incdirs_local  = src.incdirs_local,
            incdirs_system = src.incdirs_system.union(components_incdirs)
        )
        targets_srcs += tools.process(src_path_prepend)

    # Add rule for component
    target_component = Target(
        name = f"ctidy-component/{comp.path}/{comp.name}.lock",
        rule = RULE_TOUCH_AFTER, # Touch the lock file when all sources checked correctly
        deps = targets_srcs
    )

    return targets_comp + (target_component,)


def check_process_executable(tools: Toolchain, exe: Executable):
    tools.log.info(f"Add check for C executable: {exe.name}")
    #tools.log.info(f" -- Executable sources:    {[x.path for x in exe.srcs]}")
    #tools.log.info(f" -- Executable components: {[x.name for x in exe.components]}")
    
    targets = tuple()

    # Process sources
    for src in exe.srcs:
        targets += tools.process(src)

    # Process components
    for comp in exe.components:
        tools.log.info(f" --> Configure component: {comp.name}")
        targets += tools.process(comp)

    return targets


######################################
# GCC Toolchain processors
######################################


def gcc_process_source(tools: Toolchain, src: Source):
    tools.log.info (f"Adding C source: {src.path}")
    tools.log.debug(f" -- Source lang: {src.lang}")

    target = Target(
        name    = f"obj/{src.path.resolve()}.o",
        rule    = RULE_CC,
        #deps    = frozenset({str(src.path.resolve())}),
        deps    = (str(src.path.resolve()),),

        vars    = TargetVars.from_args(
            incdirs = f"-iquote {src.path.parent.resolve()}" + "".join(map(lambda x: f" -iquote {x!s}", src.incdirs_local)) + "".join(map(lambda x: f" -I {x!s}", src.incdirs_system))
        )
    )

    return (target,)


def gcc_process_component(tools: Toolchain, comp: Component):
    tools.log.info(f"Add component: {comp.name}")
    tools.log.debug(f" -- Path: {comp.path}")

    targets_srcs       = tuple()
    targets_comp       = tuple()
    components_incdirs = set()

    # Process components
    for sub_comp in comp.components_dependencies:
        components_incdirs.add(sub_comp.path.resolve())

        targets_comp += tools.process(sub_comp)
    components_incdirs = frozenset(components_incdirs)

    # Prepend component path to sources
    for src in comp.srcs:
        src_path_prepend = Source(
            path = comp.path / src.path,
            lang = src.lang,

            incdirs_local  = src.incdirs_local.union(frozenset({
                comp.path
            })),

            incdirs_system = src.incdirs_system.union(components_incdirs)
        )

        targets_srcs += tools.process(src_path_prepend)


    # Create static library target
    target_lib = Target(
        name = f"component/{comp.name}.a",
        rule = RULE_LIB,
        deps = targets_srcs
    )

    return (target_lib,) + targets_comp

def gcc_process_executable(tools: Toolchain, exe: Executable):
    tools.log.info(f"Add executable: {exe.name}")

    targets            = tuple()
    components_incdirs = set()

    # Process components
    for comp in exe.components:
        targets += tools.process(comp)
        components_incdirs.add(comp.path.resolve())
    components_incdirs = frozenset(components_incdirs)


    # Process sources
    for src in exe.srcs:
        # Include component directories to sources
        src = Source(
            path           = src.path,
            lang           = src.lang,
            incdirs_local  = src.incdirs_local,
            incdirs_system = src.incdirs_system.union(components_incdirs)
        )

        targets += tools.process(src)

    # Add executable target
    target_exe = Target(
        name = exe.name,
        rule = RULE_LD,
        deps = targets
    )

    return (target_exe,)


######################################
# Check Toolchain definition
######################################

check_toolchain = Toolchain()
check_toolchain.processor_register(Source,     check_process_source    )
check_toolchain.processor_register(Component,  check_process_component )
check_toolchain.processor_register(Executable, check_process_executable)

gcc_toolchain = Toolchain()
gcc_toolchain.processor_register  (Source,     gcc_process_source       )
gcc_toolchain.processor_register  (Component,  gcc_process_component    )
gcc_toolchain.processor_register  (Executable, gcc_process_executable   )

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
    "main_app",

    components = frozenset({
        main_component
    })
)


targets_check = check_toolchain.process(main_app)
check_toolchain.log.info("-------------------------------------")
targets_gcc   = gcc_toolchain.process  (main_app)

# Add Phony check_all target
target_check_all = Target(
    name = "check",
    rule = Phony(),
    deps = targets_check
)

targets_build = Target(
    name = "build",
    rule = Phony(),
    deps = targets_gcc
)

Path("build").mkdir(exist_ok=True)
with open("build/check.ninja", "w") as fhandle:
    uninja.output(fhandle, frozenset({target_check_all}))

with open("build/build.ninja", "w") as fhandle:
    uninja.output(fhandle, (targets_build,))