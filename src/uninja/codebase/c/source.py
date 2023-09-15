"""
========================================================
Represents a source file in the C toolset representation
========================================================
:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: July 2023
"""

from dataclasses import dataclass, field
from pathlib     import Path

from enum import Enum

from typing import FrozenSet, Optional

from .define import Define

class SourceLang(Enum):
    C      = "c",
    Header = "header",
    ASM    = "asm"


@dataclass(eq=True, frozen=True)
class Source:
    """
    Represents a source file
    """
    path: Path
    lang: SourceLang

    incdirs_local: Optional[FrozenSet[Path]]  = field(default_factory=frozenset) # List of include directories
    incdirs_system: Optional[FrozenSet[Path]] = field(default_factory=frozenset) # List of system include directories

    defines: FrozenSet[Define]                = field(default_factory=frozenset)