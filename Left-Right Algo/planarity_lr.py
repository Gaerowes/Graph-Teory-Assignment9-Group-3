import sys

sys.setrecursionlimit(100000)


class Interval:
    # A range of return edges, stored as its lowest and highest edge
    def __init__(self, low=None, high=None):
        self.low = low
        self.high = high

    def empty(self):
        return self.low is None and self.high is None

    def copy(self):
        return Interval(self.low, self.high)


class ConflictPair:
    # Two intervals that must lie on opposite sides (left / right)
    def __init__(self, left=None, right=None):
        self.left = left or Interval()
        self.right = right or Interval()

    def swap(self):
        self.left, self.right = self.right, self.left


def read_graph(path):
    # Read an edge list: one "u v" pair per line, '#' starts a comment
    adj = {}
    for line in open(path):
        p = line.split()
        if len(p) < 2 or line.startswith("#"):
            continue
        u, v = p[0], p[1]
        adj.setdefault(u, set())
        adj.setdefault(v, set())
        if u != v:
            adj[u].add(v)
            adj[v].add(u)
    return {u: sorted(vs) for u, vs in adj.items()}


def is_planar(adj):
    n = len(adj)
    m = sum(len(vs) for vs in adj.values()) // 2
    if n > 2 and m > 3 * n - 6:
        return False

    height, lowpt, lowpt2, nesting = {}, {}, {}, {}
    parent_edge, oriented = {}, set()
    out = {v: [] for v in adj}

    # Phase 1: DFS orientation. Compute heights, lowpoints and nesting depth
    def orient(v):
        e = parent_edge.get(v)
        for w in adj[v]:
            if (v, w) in oriented or (w, v) in oriented:
                continue
            vw = (v, w)
            oriented.add(vw)
            out[v].append(w)
            lowpt[vw] = lowpt2[vw] = height[v]
            if w not in height:
                parent_edge[w] = vw
                height[w] = height[v] + 1
                orient(w)
            else:
                lowpt[vw] = height[w]
            nesting[vw] = 2 * lowpt[vw]
            if lowpt2[vw] < height[v]:
                nesting[vw] += 1
            if e is not None:
                if lowpt[vw] < lowpt[e]:
                    lowpt2[e] = min(lowpt[e], lowpt2[vw])
                    lowpt[e] = lowpt[vw]
                elif lowpt[vw] > lowpt[e]:
                    lowpt2[e] = min(lowpt2[e], lowpt[vw])
                else:
                    lowpt2[e] = min(lowpt2[e], lowpt2[vw])

    for v in adj:
        if v not in height:
            height[v] = 0
            orient(v)

    ordered = {v: sorted(out[v], key=lambda w, v=v: nesting[(v, w)]) for v in adj}

    # Phase 2: testing. Stack S holds conflict pairs of return edges
    S = []
    stack_bottom, lowpt_edge, ref = {}, {}, {}

    def top():
        return S[-1] if S else None

    def lowest(P):
        if P.left.empty():
            return lowpt[P.right.low]
        if P.right.empty():
            return lowpt[P.left.low]
        return min(lowpt[P.left.low], lowpt[P.right.low])

    def conflicting(iv, b):
        return not iv.empty() and lowpt[iv.high] > lowpt[b]

    def add_constraints(ei, e):
        P = ConflictPair()
        # Merge return edges of ei into P.right
        while True:
            Q = S.pop()
            if not Q.left.empty():
                Q.swap()
            if not Q.left.empty():
                return False
            if lowpt[Q.right.low] > lowpt[e]:
                if P.right.empty():
                    P.right = Q.right.copy()
                else:
                    ref[P.right.low] = Q.right.high
                P.right.low = Q.right.low
            else:
                ref[Q.right.low] = lowpt_edge[e]
            if top() is stack_bottom[ei]:
                break
        # Merge conflicting return edges of earlier siblings into P.left
        while S and (conflicting(S[-1].left, ei) or conflicting(S[-1].right, ei)):
            Q = S.pop()
            if conflicting(Q.right, ei):
                Q.swap()
            if conflicting(Q.right, ei):
                return False
            ref[P.right.low] = Q.right.high
            if Q.right.low is not None:
                P.right.low = Q.right.low
            if P.left.empty():
                P.left = Q.left.copy()
            else:
                ref[P.left.low] = Q.left.high
            P.left.low = Q.left.low
        if not (P.left.empty() and P.right.empty()):
            S.append(P)
        return True

    def trim(u):
        # Remove back edges that return to u, the parent of the current edge
        while S and lowest(S[-1]) == height[u]:
            S.pop()
        if S:
            P = S.pop()
            while P.left.high is not None and P.left.high[1] == u:
                P.left.high = ref.get(P.left.high)
            if P.left.high is None and P.left.low is not None:
                ref[P.left.low] = P.right.low
                P.left.low = None
            while P.right.high is not None and P.right.high[1] == u:
                P.right.high = ref.get(P.right.high)
            if P.right.high is None and P.right.low is not None:
                ref[P.right.low] = P.left.low
                P.right.low = None
            S.append(P)

    def test(v):
        e = parent_edge.get(v)
        for w in ordered[v]:
            ei = (v, w)
            stack_bottom[ei] = top()
            if parent_edge.get(w) == ei:
                if not test(w):
                    return False
            else:
                lowpt_edge[ei] = ei
                S.append(ConflictPair(right=Interval(ei, ei)))
            if lowpt[ei] < height[v]:
                if w == ordered[v][0]:
                    lowpt_edge[e] = lowpt_edge[ei]
                elif not add_constraints(ei, e):
                    return False
        if e is not None:
            trim(e[0])
        return True

    for v in adj:
        if parent_edge.get(v) is None and height[v] == 0:
            if not test(v):
                return False
    return True


if __name__ == "__main__":
    g = read_graph(sys.argv[1])
    print("PLANAR" if is_planar(g) else "NON-PLANAR")
