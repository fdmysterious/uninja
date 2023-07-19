"""
===========================================================
uNinja: minimal build toolkit around the ninja build system
===========================================================

:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: July 2023

See the LICENSE file for licensing info for this specific part
"""

##########################################
# Some handy imports
##########################################

from .target import Target, TargetVar, TargetVars
from .rule   import Rule, Phony
from .output import build_file as output