#include <stdlib.h>
#include <stdio.h>

#include <bar.h>

#include "foo.h"

void foo_function(void)
{
    printf("Hello world from foo module!\n");
}

void foo_function_2(int param_a, int param_b)
{
    int result = bar(param_a, param_b);
    printf("Foo calling to bar: a=%d, b=%d => result = %d\n", param_a, param_b, result);
}