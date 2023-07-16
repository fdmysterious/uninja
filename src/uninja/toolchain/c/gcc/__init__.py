"""
========================
GCC Toolchain definition
========================

:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: July 2023
"""

from dataclasses           import dataclass
from typing                import Optional, Tuple
from pathlib               import Path

from uninja.codebase.c     import Source, SourceLang, Component, Executable
from uninja.toolchain.base import Toolchain

from uninja                import  Target, TargetVars, Rule

@dataclass
class ToolchainGCC:
    variant: Optional[str] = None
    path: Optional[Path]   = None

    cflags: Tuple[str]     = tuple()

    def __post_init__(self):
        # Build prefix
        self.prefix = ""
        if self.path is not None:
            self.prefix += str(self.path.resolve()) + "/"
        if self.variant is not None:
            self.prefix += str(self.variant) + "-"


        # Init. Rules
        self.rule_cc = Rule(
            name        = f"cc-{self.variant or 'gcc'}",
            description = "Building $in...",
            command     = f"{self.prefix}gcc -fdiagnostics-color=always -MMD -MF $out.d {' '.join(self.cflags)} $incdirs -c $in -o $out",
            depfile     = "$out.d"
        )

        self.rule_ld = Rule(
            name        = f"ld-{self.variant or 'gcc'}",
            description = "Linking $out",
            command     = f"{self.prefix}gcc -o $out $in"
        )

        self.rule_lib = Rule(
            name        = f"lib-{self.variant or 'gcc'}",
            description = "Creating static lib $out",
            command     = "ar rcs $out $in"
        )


    ############################################
    # Processors
    ############################################

    def process_source(self, tools: Toolchain, src: Source):
        tools.log.info(f"Add C source: {src.path}")
        tools.log.debug(f" -- Source lang: {src.lang}")

        target = Target(
            name = f"obj/{src.path.resolve().relative_to(tools.root_dir)}.o",
            rule = self.rule_cc,
            deps = (src.path.resolve(),),

            vars = TargetVars.from_args(
                incdirs = f"-iquote {src.path.parent.resolve()}" \
                    + "".join(map(lambda x: f" -iquote {x!s}", src.incdirs_local)) \
                    + "".join(map(lambda x: f" -I {x!s}", src.incdirs_system))
            )
        )

        return (target,)

    def process_component(self, tools: Toolchain, comp: Component):
        tools.log.info(f"Add component: {comp.name}")
        tools.log.debug(f" -- Path: {comp.path}")

        targets_srcs       = tuple()
        targets_comp       = tuple()
        components_incdirs = set()

        # Process component deps.
        for sub_comp in comp.components_dependencies:
            components_incdirs.add(sub_comp.path.resolve())
            targets_comp += tools.process(sub_comp)
        components_incdirs = frozenset(components_incdirs)

        # Process sources
        for src in comp.srcs:
            # Prepend component path to sources path
            # -> Source path is relative to component path
            # in component definition
            src_path_prepend = Source(
                path = comp.path / src.path,
                lang = src.lang,

                incdirs_local  = src.incdirs_local.union(frozenset({
                    comp.path
                })),

                incdirs_system = src.incdirs_system.union(components_incdirs)
            )

            targets_srcs += tools.process(src_path_prepend)

        # Create static library target for component
        target_lib = Target(
            name = f"component/{comp.name}.a",
            rule = self.rule_lib,
            deps = targets_srcs
        )

        return (target_lib,) + targets_comp

    def process_executable(self, tools: Toolchain, exe: Executable):
        tools.log.info(f"Add executable: {exe.name}")

        targets            = tuple()
        components_incdirs = set()

        # Process component deps
        for comp in exe.components:
            targets += tools.process(comp)
            components_incdirs.add(comp.path.resolve())
        components_incdirs = frozenset(components_incdirs)

        # Process sources
        for src in exe.srcs:
            # Include component directories to sources
            src = Source(
                path = src.path,
                lang = src.lang,
                incdirs_local  = src.incdirs_local,
                incdirs_system = src.incdirs_system.union(components_incdirs)
            )

            targets += tools.process(src)

        # Add executable target
        target_exe = Target(
            name = exe.name,
            rule = self.rule_ld,
            deps = targets
        )

        return (target_exe,)

    def associate_to(self, tools: Toolchain):
        tools.processor_register(Source,     self.process_source    )
        tools.processor_register(Component,  self.process_component )
        tools.processor_register(Executable, self.process_executable)