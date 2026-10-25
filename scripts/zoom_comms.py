"""Precompute cross-rank gravity pair counts for the partitioning demo.

Toy 3D zoom: a 32^3 background grid whose central cell (the void) holds a
16^3 grid of zoom cells. Ranks get equal azimuthal wedges around the zoom
region (about the z axis), so every rank owns some zoom cells *and* the
background around them: the worst case. A pair of cells interacts if their
minimum separation is below the gravity distance r, and every interacting
pair split across two ranks is a communication.

Output: for each rank count, a histogram (per pair type) of the minimum
separation of cross-rank pairs, so the slide can sum it up to any r.
Distances are in zoom-cell widths (3.17 Mpc for the 3.2 Gpc / 30 Mpc test
zoom). Non-periodic (the box edges are far from the zoom region anyway).

Usage: python3 scripts/zoom_comms.py  ->  components/zoom_comms.json
"""

import json
from pathlib import Path

import numpy as np

NB, NZ = 32, 16  # background cells per side, zoom cells per side
VOID = NB // 2
RANKS = [2, 4, 8, 16, 32, 64]
BIN = 0.25  # histogram bin [zoom cell widths]
RMAX = 20.0  # largest gravity distance on the slider [zoom cell widths]
NBIN = int(RMAX / BIN)
CENTRE = VOID * NZ + NZ / 2


def cells(n, w, origin):
    """Lower corners of an n^3 grid of cells of width w."""
    i = np.arange(n)
    x, y, z = np.meshgrid(i, i, i, indexing="ij")
    return np.stack([x, y, z], -1).reshape(-1, 3) * w + origin, w


def rank(lo, w, n):
    c = lo + w / 2
    ang = np.arctan2(c[:, 1] - CENTRE, c[:, 0] - CENTRE) + np.pi
    return np.minimum((ang / (2 * np.pi) * n).astype(int), n - 1)


def gap(lo_a, wa, lo_b, wb):
    """Minimum separation between axis-aligned cubes (broadcasts)."""
    d = np.maximum(0, np.maximum(lo_a - (lo_b + wb), lo_b - (lo_a + wa)))
    return np.sqrt((d**2).sum(-1))


bkg, wb = cells(NB, NZ, np.zeros(3))
ijk = (bkg / NZ).astype(int)
bkg = bkg[~np.all(ijk == VOID, axis=1)]  # the void's work lives in its zoom cells
zoom, wz = cells(NZ, 1, np.full(3, VOID * NZ))

# only background cells within RMAX of the void can talk to a zoom cell
near = bkg[gap(bkg, wb, np.full(3, VOID * NZ), NZ) < RMAX]

out = {"bin": BIN, "ranks": RANKS, "hist": {}}
for n in RANKS:
    rb, rz, rn = rank(bkg, wb, n), rank(zoom, wz, n), rank(near, wb, n)
    h = {}

    # zoom-zoom: all unique pairs
    a, b = np.triu_indices(len(zoom), 1)
    d = gap(zoom[a], wz, zoom[b], wz)
    m = (rz[a] != rz[b]) & (d < RMAX)
    h["zz"] = np.bincount((d[m] / BIN).astype(int), minlength=NBIN)[:NBIN]

    # zoom-background: every near background cell against every zoom cell
    d = gap(near[:, None], wb, zoom[None], wz)
    m = (rn[:, None] != rz[None]) & (d < RMAX)
    h["zb"] = np.bincount((d[m] / BIN).astype(int), minlength=NBIN)[:NBIN]

    # background-background: cells 3 apart are 32 > RMAX away, so offsets of 2 suffice
    key = {tuple(v): k for k, v in enumerate((bkg / NZ).astype(int))}
    acc = np.zeros(NBIN, int)
    for off in np.argwhere(np.ones((5, 5, 5))) - 2:
        if tuple(off) <= (0, 0, 0):  # count each unordered pair once
            continue
        dist = np.sqrt((np.maximum(np.abs(off) - 1, 0) ** 2).sum()) * NZ
        if dist >= RMAX:
            continue
        other = (bkg / NZ).astype(int) + off
        j = np.array([key.get(tuple(o), -1) for o in other])
        ok = j >= 0
        cross = (rb[ok] != rb[j[ok]]).sum()
        acc[int(dist / BIN)] += cross
    h["bb"] = acc

    out["hist"][n] = {k: v.tolist() for k, v in h.items()}

# self-check: with one rank nothing would cross, and more ranks never fewer comms
tot = [sum(sum(v) for v in out["hist"][n].values()) for n in RANKS]
assert all(x <= y for x, y in zip(tot, tot[1:])), tot

dest = Path(__file__).resolve().parents[1] / "components" / "zoom_comms.json"
dest.write_text(json.dumps(out))
print(f"wrote {dest}: total cross-rank pairs at r={RMAX}: {dict(zip(RANKS, tot))}")
