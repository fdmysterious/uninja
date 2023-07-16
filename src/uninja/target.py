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
from typing import Set, Optional, Dict, Callable, FrozenSet, Tuple

from .rule import Rule

import logging

log = logging.getLogger("target")

@dataclass(eq=True, frozen=True)
class TargetVar:
    key: str
    value: str

@dataclass(eq=True, frozen=True)
class TargetVars:
    values: FrozenSet[TargetVar] = field(default_factory=frozenset)

    @classmethod
    def from_args(cls, **kwargs):
        return cls(frozenset({
            TargetVar(k,v) for k,v in kwargs.items()
        }))


    def get(self, key: str):
        try:
            return next(filter(lambda x: x.key == key, self._values))
        except StopIteration:
            return None


    def assign(self, key: str, value: str):
        old_var = self.get(key)

        # This is kinda dirty...
        self.values = (self.values.difference(old_var) if old_var is not None else self.values).union(TargetVar(key,value))


    def append(self, key: str, value: str):
        var = self.get(key)
        
        if var is not None:
            var.value += " " + value
        else:
            var = TargetVar(key, value)

        self.assign(key, var.value)


@dataclass(eq=True, frozen=True)
class Target:
    name: str
    rule: Rule
    #deps: FrozenSet["Target" ] = field(default_factory=frozenset)

    # Note 2023-07-16: deps cannot be a FrozenSet, as the order must be kept. This is the
    # responsability of the toolchain to ensure no duplicate entry is added.
    deps: Tuple["Target"] = field(default = tuple())

    # This is not a dict as it's not hashable. There seems to be
    # some trickery, like https://stackoverflow.com/questions/1151658/python-hashable-dicts,
    # but this is somehow complex for nothing.
    vars: TargetVars = field(default_factory=TargetVars)


    def __str__(self):
        return self.name

    def is_phony(self):
        return isinstance(self.rule, Phony)