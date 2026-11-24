/* Second, independent float64 reference: the C library's scalar double
 * functions, applied elementwise.  Built by sweep.py with
 *   gcc -O2 -fno-builtin -fno-fast-math -shared -fPIC ref_libm.c -o ref_libm.so -lm
 */
#include <math.h>
#include <stddef.h>

typedef double (*fn)(double);

static fn table[] = {
    exp, exp2, expm1, log, log2, log10, log1p,
    sin, cos, tan, asin, acos, atan,
    sinh, cosh, tanh, asinh, acosh, atanh,
    cbrt, sqrt,
};

void apply(int id, const double *in, double *out, size_t n)
{
    fn f = table[id];
    for (size_t i = 0; i < n; i++)
        out[i] = f(in[i]);
}
