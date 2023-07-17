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

from conf.toolchain import tools_build, tools_check
from workspace      import export as main_targets


################################
# Process targets
################################

targets = reduce(
    lambda a,b: a+b,
    map(tools_build.process, main_targets)
)

targets_check = reduce(
    lambda a,b: a+b,
    map(tools_check.process, main_targets)
)


################################
# Save to output file
################################
tools_build.build_dir.mkdir(exist_ok=True)
with open(f"{tools_build.build_dir}/build.ninja", "w") as fhandle:
    uninja.output(fhandle, targets)

tools_check.build_dir.mkdir(exist_ok=True)
with open(f"{tools_check.build_dir}/check.ninja", "w") as fhandle:
    uninja.output(fhandle, targets_check)