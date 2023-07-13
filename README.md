Minimal build system around `ninja`
===================================

- Florian Dupeyron <florian.dupeyron@mugcat.fr>
- July 2023, based on source code from September 2018


# What is this thing?

uNinja is a simple build system toolkit structured around [ninja](https://ninja-build.org/).
Its goal is to give the user some simple helpers to generate ninja build files, using a convenient modular
structure, and the python language for flexible configuration.

# Give me an example?

At its lowest level, you can generate a simple build file for a C hello world application
as follows:

```python
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
        deps = [dep_path]
    )

def exe(name, srcs):
    print(f"\nAdd executable {name}")

    objs = [obj(src) for src in srcs]

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
```

The following script can be ran:

```python
$ ~/workspace/uninja/example_project  
> python3 gen.py 

Add executable main
 -- Add object target /home/username/workspace/uninja/example_project/src/main.c
```

And the resulting `build/build.ninja` file:

```ninja
rule cc
    command = gcc -fdiagnostics-color=always -MMD -MF $out.d -c $in -o $out
    description = Building object $in

rule ld
    command = gcc -o $out $in
    description = Linking $out

build obj//home/username/workspace/uninja/example_project/src/main.c.o : cc /home/username/workspace/uninja/example_project/src/main.c 

build bin/main : ld obj//home/username/workspace/uninja/example_project/src/main.c.o 
```

Running the following commands:

```bash
$ ~/workspace/uninja/example_project  
> cd build/
(.env) 
$ ~/workspace/uninja/example_project/build  
> ninja
[2/2] Linking bin/main
(.env) 
$ ~/workspace/uninja/example_project/build  
> 
```

Should create the `bin/main` file:

```bash
$ ~/workspace/uninja/example_project/build  
> ./bin/main 
Hello world!
```

# Actual use cases

- Build _scenarii_ not covered by already existing tools (CMake, meson, cargo, GNAT, _etc._)
- Maniac users who want to control everything that's generated
- Fun?