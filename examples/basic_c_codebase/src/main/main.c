#include <stdlib.h>
#include <stdio.h>

#include <bar.h>
#include <foo.h>

int main(int argc, char* argv[])
{
    /* Unused parameters */
    (void)argc;
    (void)argv;

    foo_function();

    const int param_a  = 3;
    const int param_b  = 5;

    int result_c = bar(param_a,param_b);

    printf("The result of the bar operation with a = %d and b = %d is: %d\n", param_a,param_b,result_c);

    foo_function_2(param_a, param_b);

    return EXIT_SUCCESS;
}