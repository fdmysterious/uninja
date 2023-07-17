"""
=======================================
Representation of a preprocessor define
=======================================

:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: July 2023
"""

from dataclasses import dataclass
from typing      import Optional

@dataclass(eq=True, frozen=True)
class Define:
    name: str
    value: Optional[str] = None