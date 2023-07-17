"""
=+===============================
Model definition for a C codebase
=================================
:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: July 2023
"""

from .define     import Define
from .source     import Source, SourceLang
from .component  import Component
from .executable import Executable
from .static_lib import StaticLib

from pathlib import Path

#######################################################
# Helper function to declare C Codebase elements
#######################################################

def add_source(
    path: Path,
    lang: SourceLang = None,

    incdirs_local  = {},
    incdirs_system = {},

    defines        = {},

    node_type = Source
):
    """
    Adds a source to the project.
    :param path: Path to source relative to component path,
    :param lang: Set explicit lang. If not indicated, is deduced  from file extension.
    """
    EXTENSIONS_DICT = {
        ".c":   SourceLang.C,
        ".s":   SourceLang.ASM,
        ".asm": SourceLang.ASM
    }

    # Convert arguments
    path           = Path(path)
    incdirs_local  = frozenset(incdirs_local )
    incdirs_system = frozenset(incdirs_system)

    # Process defines
    def process_define(x):
        if isinstance(x, str):
            return Define(name=x)
        elif isinstance(x, tuple):
            return Define(name = x[0], value=x[1])
        elif isinstance(x, Define):
            return x
        else:
            raise TypeError(f"Unexpected type for define: {x} -> {type(x)}")
    defines = frozenset(map(process_define, defines))

    # Try to deduce extension from file name
    if lang is None:
        try:
            lang = EXTENSIONS_DICT[path.suffix]
        except KeyError:
            raise KeyError("Cannot deduce file lang from extension: {path}")

    return node_type(
        path           = path,
        lang           = lang,
        incdirs_local  = incdirs_local,
        incdirs_system = incdirs_system,
        defines        = defines
    )


def add_component(
    name: str,
    path: Path,

    srcs                    = {},
    interface_directories   = {},
    components_dependencies = {},

    node_type = Component
):
    # Convert arguments
    name                    = str(name)
    path                    = Path(path)

    interface_directories   = frozenset(interface_directories)
    components_dependencies = frozenset(components_dependencies)

    # Process sources
    srcs = frozenset({
        add_source(x) if (isinstance(x, str) or isinstance(x, Path)) else x
        for x in srcs
    })

    # Create component object
    return node_type(
        name                    = name,
        path                    = path,
        srcs                    = srcs,
        interface_directories   = interface_directories,
        components_dependencies = components_dependencies
    )

def add_executable(
    name: str,

    srcs       = {},
    components = {},

    node_type  = Executable
):
    # Convert arguments
    name       = str(name)
    srcs       = frozenset(srcs)
    components = frozenset(components)

    # Create object
    return node_type(
        name       = name,
        srcs       = srcs,
        components = components
    )

def add_static_lib(
    name: str,
    srcs = {},
    components = {},

    node_type = StaticLib
):
    # Convert arguments
    name       = str(name)
    srcs       = frozenset(srcs)
    components = frozenset(components)

    # Create object
    return node_type(
        name       = name,
        srcs       = srcs,
        components = components
    )