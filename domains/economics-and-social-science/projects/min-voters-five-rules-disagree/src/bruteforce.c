/* Exhaustive check, independent of the integer programs and of rules.py.
 *
 *   ./bruteforce M N [robust]
 *
 * Enumerates every profile (multiset of strict rankings of M candidates)
 * with at most N voters, evaluates the five rules directly, and prints, for
 * every set of at least two rules, the smallest number of voters at which
 * the rules in the set elect pairwise different candidates ("-" if none up
 * to N). By default a rule has a winner only if no tie occurs at any of its
 * steps (the README's strict convention; Hare runs until one candidate is
 * left). Rule bits: P=1 R=2 H=4 B=8 C=16.
 *
 * With a third argument the "robust" convention is used for the runoff and
 * for Hare: ties are allowed, and the rule has a winner iff the same
 * candidate wins however the ties are broken.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXR 120
static int M, N, R, ROBUST;
static int rk[MAXR][5], pos[MAXR][5];
static int top[MAXR][32];          /* top[r][alive mask] */
static int stack_r[64], stack_k[64], depth;
static int best[32];
static unsigned long long leaves;

static void gen(int *perm, int k, int used) {
    if (k == M) {
        memcpy(rk[R], perm, sizeof(int) * M);
        for (int i = 0; i < M; i++) pos[R][perm[i]] = i;
        R++;
        return;
    }
    for (int c = 0; c < M; c++) if (!(used >> c & 1)) { perm[k] = c; gen(perm, k + 1, used | 1 << c); }
}

static void firsts(int alive, int *f) {
    for (int c = 0; c < M; c++) f[c] = 0;
    for (int i = 0; i < depth; i++) f[top[stack_r[i]][alive]] += stack_k[i];
}
static int margin(int a, int b) {
    int d = 0;
    for (int i = 0; i < depth; i++) d += pos[stack_r[i]][a] < pos[stack_r[i]][b] ? stack_k[i] : -stack_k[i];
    return d;
}

static int hare_set(int alive) {   /* bit mask of possible Hare winners */
    if (!(alive & (alive - 1))) return alive;
    int f[5], lo = 1 << 30, res = 0;
    firsts(alive, f);
    for (int c = 0; c < M; c++) if ((alive >> c & 1) && f[c] < lo) lo = f[c];
    for (int c = 0; c < M; c++) if ((alive >> c & 1) && f[c] == lo) res |= hare_set(alive & ~(1 << c));
    return res;
}
static int single(int set) {       /* the element of a one-element set, else -1 */
    if (!set || (set & (set - 1))) return -1;
    return __builtin_ctz(set);
}

static void leaf(int n) {
    int w[5], f[5], all = (1 << M) - 1;
    leaves++;
    firsts(all, f);
    /* plurality, and the two leaders for the runoff */
    int a = -1, b = -1;
    for (int c = 0; c < M; c++) {
        if (a < 0 || f[c] > f[a]) { b = a; a = c; }
        else if (b < 0 || f[c] > f[b]) b = c;
    }
    int ties_top = 0, ties_second = 0;
    for (int c = 0; c < M; c++) { if (f[c] == f[a]) ties_top++; if (f[c] == f[b]) ties_second++; }
    w[0] = ties_top == 1 ? a : -1;
    /* runoff pair is determined iff the second-highest count is strictly above the third */
    int pair_ok = (f[a] == f[b]) ? (ties_top == 2) : (ties_second == 1);
    if (pair_ok) { int d = margin(a, b); w[1] = d > 0 ? a : d < 0 ? b : -1; } else w[1] = -1;
    if (ROBUST) {
        int set = 0, amb = 0;
        for (int x = 0; x < M; x++) for (int y = x + 1; y < M; y++) {
            int possible;
            if (ties_top >= 2) possible = f[x] == f[a] && f[y] == f[a];
            else possible = (x == a && f[y] == f[b]) || (y == a && f[x] == f[b]);
            if (!possible) continue;
            int d = margin(x, y);
            if (d == 0) amb = 1; else set |= 1 << (d > 0 ? x : y);
        }
        w[1] = amb ? -1 : single(set);
    }
    /* Hare */
    int alive = all, cnt = M; w[2] = -2;
    while (cnt > 1) {
        firsts(alive, f);
        int lo = -1, nlo = 0;
        for (int c = 0; c < M; c++) if (alive >> c & 1) {
            if (lo < 0 || f[c] < f[lo]) { lo = c; nlo = 1; } else if (f[c] == f[lo]) nlo++;
        }
        if (nlo != 1) { w[2] = -1; break; }
        alive &= ~(1 << lo); cnt--;
    }
    if (w[2] == -2) for (int c = 0; c < M; c++) if (alive >> c & 1) w[2] = c;
    if (ROBUST) w[2] = single(hare_set(all));
    /* Borda */
    int s[5] = {0}, bw = 0, nb = 0;
    for (int i = 0; i < depth; i++) for (int c = 0; c < M; c++) s[c] += stack_k[i] * (M - 1 - pos[stack_r[i]][c]);
    for (int c = 1; c < M; c++) if (s[c] > s[bw]) bw = c;
    for (int c = 0; c < M; c++) if (s[c] == s[bw]) nb++;
    w[3] = nb == 1 ? bw : -1;
    /* Condorcet */
    w[4] = -1;
    for (int c = 0; c < M && w[4] < 0; c++) {
        int ok = 1;
        for (int d = 0; d < M && ok; d++) if (d != c && margin(c, d) <= 0) ok = 0;
        if (ok) w[4] = c;
    }
    for (int mask = 3; mask < 32; mask++) {
        if (best[mask] <= n) continue;
        int seen = 0, ok = 1, k = 0;
        for (int i = 0; i < 5 && ok; i++) if (mask >> i & 1) {
            k++;
            if (w[i] < 0 || (seen >> w[i] & 1)) ok = 0; else seen |= 1 << w[i];
        }
        if (ok && k >= 2) best[mask] = n;
    }
}

static void rec(int r, int n) {   /* rankings r.. still free, n voters placed */
    if (n > 0) leaf(n);          /* profile with no further voters */
    if (n == N) return;
    for (int q = r; q < R; q++)
        for (int k = 1; n + k <= N; k++) {
            stack_r[depth] = q; stack_k[depth] = k; depth++;
            rec(q + 1, n + k);
            depth--;
        }
}

int main(int argc, char **argv) {
    M = atoi(argv[1]); N = atoi(argv[2]); ROBUST = argc > 3;
    int perm[5]; gen(perm, 0, 0);
    for (int r = 0; r < R; r++) for (int mask = 1; mask < (1 << M); mask++)
        for (int i = 0; i < M; i++) if (mask >> rk[r][i] & 1) { top[r][mask] = rk[r][i]; break; }
    for (int i = 0; i < 32; i++) best[i] = 1 << 30;
    rec(0, 0);
    printf("m=%d N=%d convention=%s profiles=%llu\n", M, N, ROBUST ? "robust" : "strict", leaves);
    for (int mask = 3; mask < 32; mask++) {
        if (__builtin_popcount(mask) < 2) continue;
        char name[6]; int j = 0;
        for (int i = 0; i < 5; i++) if (mask >> i & 1) name[j++] = "PRHBC"[i];
        name[j] = 0;
        if (best[mask] < (1 << 30)) printf("%s %d\n", name, best[mask]); else printf("%s -\n", name);
    }
    return 0;
}
