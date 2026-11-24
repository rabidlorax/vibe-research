"""Baselines: prune the classical exchange networks for the median of 5, 7, 9
(the widely circulated "opt_med" kernels; typed here from memory and therefore
verified by verify.py rather than trusted) down to the min/max operations the
output actually depends on, and write them as programs.

An exchange (a, b) puts min in wire a and max in wire b.
Usage: python baseline.py   (writes ../results/baseline_median{5,7,9}.txt)
"""
NETS = {
    5: ([(0, 1), (3, 4), (0, 3), (1, 4), (1, 2), (2, 3), (1, 2)], 2),
    7: ([(0, 5), (0, 3), (1, 6), (2, 4), (0, 1), (3, 5), (2, 6), (2, 3), (3, 6),
         (4, 5), (1, 4), (1, 3), (3, 4)], 3),
    9: ([(1, 2), (4, 5), (7, 8), (0, 1), (3, 4), (6, 7), (1, 2), (4, 5), (7, 8),
         (0, 3), (5, 8), (4, 7), (3, 6), (1, 4), (2, 5), (4, 7), (4, 2), (6, 4),
         (4, 2)], 4),
}


def prune(n, exchanges, out_wire):
    ops = []                     # (op, a, b) over node ids
    wire = list(range(n))
    for a, b in exchanges:
        x, y = wire[a], wire[b]
        ops.append(("min", x, y)); wire[a] = n + len(ops) - 1
        ops.append(("max", x, y)); wire[b] = n + len(ops) - 1
    need = {wire[out_wire]}
    for i in range(len(ops) - 1, -1, -1):
        if n + i in need:
            need.update(x for x in ops[i][1:] if x >= n)
    keep = [i for i in range(len(ops)) if n + i in need]
    ren = {n + i: n + j for j, i in enumerate(keep)}
    ren.update({i: i for i in range(n)})
    return [(ops[i][0], ren[ops[i][1]], ren[ops[i][2]]) for i in keep]


if __name__ == "__main__":
    for n, (ex, w) in NETS.items():
        prog = prune(n, ex, w)
        path = f"../results/baseline_median{n}.txt"
        with open(path, "w") as f:
            f.write(f"# classical {len(ex)}-exchange median-of-{n} network, pruned by baseline.py\n")
            f.write(f"{n} {(n + 1) // 2}\n")
            for op, a, b in prog:
                f.write(f"{op} {a} {b}\n")
        print(n, "exchanges:", len(ex), "min/max ops after pruning:", len(prog))
