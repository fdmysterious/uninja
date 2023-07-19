"""
=======================================================
clang-tidy toolchain definition for some source-checks!
=======================================================
:Authors: - Florian Dupeyron <florian.duperyon@mugcat.fr>
:Date: July 2023
"""

from dataclasses           import dataclass
from pathlib               import Path

from typing                import Optional, Tuple, FrozenSet

from uninja.codebase.c     import Source, SourceLang, Component, Executable, StaticLib, Define
from uninja.toolchain.base import Toolchain

from uninja                import Target, TargetVars, Rule

@dataclass
class ToolchainClangTidy:
    checks: Tuple[str] = ("*", "-llvm*",) # List of checks that are enabled or disabled, tuple as order must be kept
    errors: Tuple[str] = ("*",)           # List of checks that are considered as errors, tuple as order must be kept

    def __post_init__(self):
        # Checks string
        checks = ",".join(self.checks)
        errors = ",".join(self.errors)

        # Init rules
        self.rule_ctidy = Rule(
            name        = "ctidy",
            description = "Checking $in...",
            command     = f"clang-tidy --quiet --header-filter=. --checks={checks} --warnings-as-errors={errors} $in -- $incdirs $defines > $out || true" 
        )

        self.rule_touch_after = Rule(
            name        = "touch_after",
            description = "Touchgin $out...",
            command     = "touch $out"
        )


    def process_source(self, tools: Toolchain, src: Source):
        tools.log.info(f"Add check for C source: {src.path}")

        target = Target(
            name = f"ctidy/{src.path.resolve().relative_to(tools.root_dir)}.log",
            rule = self.rule_ctidy,
            deps = (src.path.resolve(),),

            # FIXME # No escaping for defines, can cause some bugs?
            vars = TargetVars.from_args(
                incdirs = f"-iquote {src.path.parent.resolve()}" \
                    + "".join(map(lambda x: f" -iquote {x!s}", src.incdirs_local)) \
                    + "".join(map(lambda x: f" -I {x!s}", src.incdirs_system)),

                defines = " ".join(map(lambda x: f"-D{x.name}" + (f"={x.value}" if x.value is not None else ""), src.defines))
            )
        )

        return (target,)


    def process_component(self, tools: Toolchain, comp: Component):
        tools.log.info (f"Add check for C component: {comp.name}")
        tools.log.debug(f" -- Component path: {comp.path}")

        targets_srcs       = tuple()
        targets_comp       = tuple()
        components_incdirs = set()

        # Process components deps.
        for sub_comp in comp.components_dependencies:
            components_incdirs.add(sub_comp.path.resolve())
            targets_comp += tools.process(sub_comp)
        components_incdirs = frozenset(components_incdirs)

        # Process sources
        for src in comp.srcs:
            # Prepend path to sources paths, source path is relative to component path
            src_path_prepend = Source(
                path = comp.path / src.path,
                lang = src.lang,

                incdirs_local = src.incdirs_local.union(frozenset({
                    comp.path
                })),

                incdirs_system = src.incdirs_system.union(components_incdirs).union(map(Path.resolve, comp.interface_directories))
            )

            targets_srcs += tools.process(src_path_prepend)

        # Add phony rule for component
        target_component = Target(
            name = f"ctidy-component/{comp.path}/{comp.name}.lock",
            rule = self.rule_touch_after,
            deps = targets_srcs
        )

        return targets_comp + (target_component,)


    def process_executable_static_lib(self, tools: Toolchain, exe: Executable):
        tools.log.info(f"Add check for C executable/static lib: {exe.name}")

        targets = tuple()

        # Process sources
        for src in exe.srcs:
            targets += tools.process(src)

        # Process components
        for comp in exe.components:
            targets += tools.process(comp)

        # Add phony rule for component
        target_exe = Target(
            name = f"ctidy-binlib/{exe.name}.lock",
            rule = self.rule_touch_after,
            deps = targets
        )
        
        return (target_exe,)


    def associate_to(self, tools: Toolchain):
        tools.processor_register(Source,     self.process_source               )
        tools.processor_register(Component,  self.process_component            )
        tools.processor_register(Executable, self.process_executable_static_lib)
        tools.processor_register(StaticLib,  self.process_executable_static_lib)