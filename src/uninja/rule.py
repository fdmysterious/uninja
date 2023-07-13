"""
================
Rule declaration
================

:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: July 2023
"""

from dataclasses import dataclass, field
from typing      import Optional


@dataclass(eq=True, frozen=True)
class Rule:
    name: str
    command: str
    description: Optional[str] = None
    depfile: Optional[str]     = None

    # deps argument not supported yet
    # msvc_deps_prefix not supported yet
    # dyndep not supported yet
    # generator not supported yet
    # restat not supported yet
    # rspfile and rspfile_content not supported yet

    def __str__(self):
        return self.name

@dataclass(eq=True, frozen=True)
class Phony(Rule):
    name:        str = "phony"
    command:     str = ""