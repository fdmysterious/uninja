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
from typing import Set, Optional, Dict, Callable, FrozenSet

from .rule import Rule

import logging

log = logging.getLogger("target")

@dataclass(eq=True, frozen=True)
class Target:
    name: str
    rule: Rule
    deps: FrozenSet["Target"] = field(default_factory=frozenset)
    #vars: Optional[Dict[str, any]] = field(default_factory=dict) # FIXME

    # FIXME # Really useful?
    gen_name: Optional[Callable[[str], str]] = lambda x: x

    def __str__(self):
        return self.name

    def is_phony(self):
        return isinstance(self.rule, Phony)