"""
========================================================
Represents a source file in the C toolset representation
========================================================
:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: July 2023
"""

from dataclasses import dataclass
from pathlib     import Path

from enum import Enum

class SourceLang(Enum):
    C   = "c",
    ASM = "asm"


@dataclass(eq=True, frozen=True)
class Source:
    """
    Represents a source file
    """
    path: Path
    lang: SourceLang