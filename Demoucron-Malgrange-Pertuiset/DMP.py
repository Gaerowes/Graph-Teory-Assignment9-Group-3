"""
Planarity test with the Demoucron-Malgrange-Pertuiset (DMP) algorithm.
Usage:  python dmp.py                 (runs every input_*.txt in this folder)
        python dmp.py input_k5.txt
"""
import glob
import sys

sys.setrecursionlimit(10000)


def read(path):
    """Lecture format: a line with 1 number = node count, then node labels;
    a line with 2 numbers = an edge. Other lines (headers) are ignored."""
    adj, nums = {}, []
    for line in open(path):
        t = line.split()
        if len(t) == 1 and t[0].isdigit():
            nums.append(int(t[0]))
        elif len(t) == 2 and all(x.isdigit() for x in t):
            u, v = map(int, t)
            adj.setdefault(u, set())
            adj.setdefault(v, set())
            if u != v:                      # self-loops are dropped
                adj[u].add(v)               # sets also merge parallel edges
                adj[v].add(u)
                if nums:                                # header present: add isolated vertices
                    for v in nums[1:nums[0] + 1]:
                        adj.setdefault(v, set())
    return adj

def blocks(adj):
    """Split the graph into biconnected blocks (Tarjan, DFS + low-link)."""
    idx, low, stack, out = {}, {}, [], []

    def dfs(u, p):
        idx[u] = low[u] = len(idx)
        for w in adj[u]:
            if w == p:
                continue
            if w not in idx:
                stack.append((u, w))
                dfs(w, u)
                low[u] = min(low[u], low[w])
                if low[w] >= idx[u]:        # u separates this block
                    b = {}
                    while True:
                        a, c = stack.pop()
                        b.setdefault(a, set()).add(c)
                        b.setdefault(c, set()).add(a)
                        if (a, c) == (u, w):
                            break
                    out.append(b)
            elif idx[w] < idx[u]:           # back edge
                stack.append((u, w))
                low[u] = min(low[u], idx[w])

    for v in adj:
        if v not in idx:
            dfs(v, None)
    return out


def find_cycle(g):
    """Any cycle of g, as a list of vertices (first back edge found by DFS)."""
    par, dep = {}, {}

    def dfs(u):
        for w in g[u]:
            if w == par[u]:
                continue
            if w not in par:
                par[w], dep[w] = u, dep[u] + 1
                c = dfs(w)
                if c:
                    return c
            elif dep[w] < dep[u]:           # w is an ancestor of u
                c, x = [u], u
                while x != w:
                    x = par[x]
                    c.append(x)
                return c

    s = next(iter(g))
    par[s], dep[s] = None, 0
    return dfs(s)


def dmp(g):
    """DMP on one biconnected block g. True if planar."""
    c = find_cycle(g)
    H = set(c)                                          # drawn vertices
    E = {frozenset(e) for e in zip(c, c[1:] + c[:1])}   # drawn edges
    faces = [c, c[:]]                                   # inside and outside

    while True:
        # Fragments = (attachment vertices, inner vertices)
        # 1) chords: edges outside H with both ends in H
        chords = {frozenset((u, v)) for u in H for v in g[u] if v in H} - E
        frags = [(set(e), set()) for e in chords]
        # 2) bridges: components of g - H plus the H-vertices they touch
        seen = set(H)
        for s in g:
            if s in seen:
                continue
            comp, att, queue = {s}, set(), [s]
            seen.add(s)
            for x in queue:                             # list grows as we go
                for y in g[x]:
                    if y in H:
                        att.add(y)
                    elif y not in seen:
                        seen.add(y)
                        comp.add(y)
                        queue.append(y)
            frags.append((att, comp))

        if not frags:
            return True                                 # H == g, done

        # A fragment fits only in a face containing all its attachments.
        ok = [[i for i, f in enumerate(faces) if att <= set(f)]
            for att, _ in frags]
        if not all(ok):
            return False                                # fits nowhere
        k = min(range(len(frags)), key=lambda i: len(ok[i]))   # most constrained
        att, comp = frags[k]
        fi = ok[k][0]

        # Path a ... b through the fragment, between two attachments.
        a = min(att)
        if not comp:
            path = sorted(att)
        else:
            prev = {y: a for y in g[a] if y in comp}
            queue = list(prev)
            for x in queue:                             # BFS inside the fragment
                b = next((y for y in g[x] if y in H and y != a), None)
                if b is not None:
                    break
                for y in g[x]:
                    if y in comp and y not in prev:
                        prev[y] = x
                        queue.append(y)
            path = [b, x]
            while path[-1] != a:
                path.append(prev[path[-1]])
            path.reverse()

        # Draw the path in face fi: it splits the face in two.
        b, mid = path[-1], path[1:-1]
        f = faces[fi]
        i = f.index(a)
        f = f[i:] + f[:i]                               # rotate: a first
        j = f.index(b)
        faces[fi] = f[:j + 1] + mid[::-1]               # a..b then back on path
        faces.append(f[j:] + [f[0]] + mid)              # b..a then forward on path
        H |= set(path)
        E |= {frozenset(e) for e in zip(path, path[1:])}


def planar(adj):
    """A graph is planar iff all its biconnected blocks are planar."""
    return all(dmp(b) for b in blocks(adj) if len(b) > 2)


if __name__ == "__main__":
    for p in sys.argv[1:] or sorted(glob.glob("input_*.txt")):
        print(p, "->", "PLANAR" if planar(read(p)) else "NON-PLANAR")