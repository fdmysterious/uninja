"""
================
Target types def 
================

:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: July 2023

original source code from  September 2018
"""

from dataclasses import dataclass, field
import re
from typing import Set, Optional, Dict, Callable

from .rule import Rule

import logging

log = logging.getLogger("target")

@dataclass(eq=True, frozen=True)
class Target:
    name: str
    rule: Rule
    deps: Set["Target"] = field(default_factory=set)
    vars: Optional[Dict[str, any]] = field(default_factory=dict)

    # FIXME # Really useful?
    gen_name: Optional[Callable[[str], str]] = lambda x: x

    def __str__(self):
        return self.name