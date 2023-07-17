"""
========================
Main project directories
========================
:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: July 2023
"""

from pathlib import Path

project_dir = (Path(__file__) / ".." / "..").resolve() # First .. is for file name, second for conf dir

build_dir   = project_dir / "build"