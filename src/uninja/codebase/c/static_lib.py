"""
=======================================
Model definition for a C static library
=======================================
:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: July 2023
"""

from dataclasses import dataclass, field
from typing      import FrozenSet

from .component import Component
from .source    import Source

@dataclass(eq=True, frozen=True)
class StaticLib:
    name: str

    # Last level sources for library
    srcs: FrozenSet[Source]          = field(default_factory=frozenset)

    # Input components
    components: FrozenSet[Component] = field(default_factory=frozenset)