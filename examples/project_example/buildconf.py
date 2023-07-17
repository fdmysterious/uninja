import uninja
import logging

from pathlib import Path

from uninja.utils    import color_log
color_log.install(level=logging.INFO)

from uninja.toolchain.base  import Toolchain
from uninja.toolchain.c.gcc import ToolchainGCC

log = logging.getLogger("project config")


################################
# Project configuration
################################

from functools      import reduce

from conf.toolchain import tools
from workspace      import export as main_targets


################################
# Process targets
################################

targets = reduce(
    lambda a,b: a+b,
    map(tools.process, main_targets)
)


################################
# Save to output file
################################
tools.build_dir.mkdir(exist_ok=True)

with open(f"{tools.build_dir}/build.ninja", "w") as fhandle:
    uninja.output(fhandle, targets)