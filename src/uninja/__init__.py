"""
===========================================================
uNinja: minimal build toolkit around the ninja build system
===========================================================

:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: July 2023
"""

##########################################
# Some handy imports
##########################################

from .target import Target
from .rule   import Rule
from .output import build_file as output