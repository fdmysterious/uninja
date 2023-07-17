from uninja.codebase import c as c_code

################################
# Components declaration
################################

bar = c_code.add_component(
    name = "bar",
    path = "src/bar",
    srcs = {
        "bar.c",
    }
)

foo = c_code.add_component(
    name = "foo",
    path = "src/foo",
    srcs = {
        "foo.c"
    },

    components_dependencies = {
        bar
    }
)

main = c_code.add_component(
    name = "main",
    path = "src/main",
    srcs = {
        "main.c"
    },

    components_dependencies = {
        bar, foo
    }
)

exe = c_code.add_executable(
    name       = "bin/main",
    components = {
        main
    }
)

# Exported target
export = (exe,)