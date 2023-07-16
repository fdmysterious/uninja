"""
==================================
Base classes to define a toolchain
==================================

:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: - July 2023
"""


import logging

from pathlib     import Path

from dataclasses import dataclass, field
from typing      import Dict, Tuple, Type, Callable, FrozenSet

from ..          import Target, Rule


@dataclass
class Toolchain:
    # Root project dir
    root_dir: Path

    # Build dir
    build_dir: Path

    # The processors toolchain takes an input argument corresponding to a node graph
    # containing the specialized item node (a C source, or COmponent for example). It
    # returns the resulting set of generated Targets and Rules.
    processors: Dict[Type,Callable[["Toolchain", any], Tuple[Target]]] = field(default_factory=dict)

    # User settings that can be used by processor functions
    settings: Dict[str, any] = field(default_factory=dict)

    
    def __post_init__(self):
        self.log = logging.getLogger(f"toolchain")


    def process(self, x: any) -> Tuple[Target]:
        processor = self.processors.get(type(x), None)

        if processor is None:
            raise KeyError(f"No processor has been registered for item type: {type(x)}")

        return processor(self, x)


    def processor_register(self, x: Type, processor: Callable[["Toolchain", any], Tuple[Target]]):
        if x in self.processors:
            raise KeyError(f"Processor already register for type {x}")
        self.processors[x] = processor