"""
========================
Represents a C component
========================

:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: July 2023
"""

from dataclasses import dataclass, field
from pathlib     import Path
from typing      import FrozenSet, Optional

from .source     import Source
from .define     import Define

@dataclass(eq=True, frozen=True)
class Component:
    name: str
    path: Path

    # List of input source files
    srcs: FrozenSet[Source]

    # Some defines for all the component
    defines: FrozenSet[Define]

    # List of interface include directories
    # -> If a relative path is given, it is relative
    # to the path of the component.
    interface_directories: FrozenSet[Path] = field(default_factory=frozenset)

    # List of component dependencies (libs, etc.)
    components_dependencies: FrozenSet["Component"] = field(default_factory=frozenset)