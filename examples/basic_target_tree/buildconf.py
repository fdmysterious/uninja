import uninja
from pathlib       import Path


#################################
# Rules defintion
#################################
CC = uninja.Rule(
    name        = "cc",
    description = "Building object $in",
    command     = "gcc -fdiagnostics-color=always -MMD -MF $out.d -c $in -o $out",
)

LD = uninja.Rule(
    name        = "ld",
    description = "Linking $out",
    command     = f"gcc -o $out $in"
)


#################################
# Target helpers
#################################
def obj(x):
    """
    Creates an object target for the given source file
    """

    # Resolve to absolute path to avoid relative path problems if putting build.ninja in separate build folder
    # but do not forget to add a default guard
    dep_path = x.resolve() if isinstance(x, Path) else str(x)

    print(f" -- Add object target {dep_path}")

    return uninja.Target(
        name = f"obj/{dep_path}.o",
        rule = CC,
        deps = (dep_path,)
    )

def exe(name, srcs):
    print(f"\nAdd executable {name}")

    objs = (obj(src) for src in srcs)

    return uninja.Target(
        name = f"bin/{name}",
        rule = LD,
        deps = objs
    )

#################################
# Define the targets
#################################

main_exe = exe(
    "main",
    srcs = [
        Path("src/main.c")
    ]
)

#################################
# Export ninja file
#################################
Path("build").mkdir(exist_ok=True)
with open("build/build.ninja", "w") as fhandle:
    uninja.output(fhandle, [main_exe])