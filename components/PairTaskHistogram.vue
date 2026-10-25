<script setup>
// Toy model of zoom-cell gravity pairs. Every pair of 16^3 zoom cells is binned
// by the minimum distance between the two cells:
//   d < min(r_FMM, r_mesh)        -> pair task (needs splitting / direct work)
//   r_FMM <= d < r_mesh            -> multipole (M2L) only
//   d >= r_mesh                    -> handled by the mesh, no task at all
// Cell size and mesh cut-offs follow the 3.2 Gpc / 30 Mpc test zoom.
import { computed, ref } from 'vue'

const N = 16
const W = 3.17 // zoom cell width [Mpc]
const R_FMM = 9.5 // fixed, illustrative [Mpc]
const PRESETS = [
  { label: 'global mesh only', r: 17.6 },
  { label: '+ zoom mesh', r: 1.7 },
]
const logR = ref(Math.log10(17.6))
const rMesh = computed(() => 10 ** logR.value)

// pair counts by integer offset are cheap: count(d) = prod(N - |d_i|)
const pairs = (() => {
  const out = []
  for (let i = 0; i < N; i++)
    for (let j = 0; j < N; j++)
      for (let k = 0; k < N; k++) {
        if (i + j + k === 0) continue
        const mult = (i ? 2 : 1) * (j ? 2 : 1) * (k ? 2 : 1) / 2 // +/- offsets, unordered
        const n = (N - i) * (N - j) * (N - k) * mult
        const g = (x) => Math.max(x - 1, 0)
        out.push({ d: W * Math.hypot(g(i), g(j), g(k)), n })
      }
  return out
})()

const BIN = W
const NB = Math.ceil(Math.max(...pairs.map((p) => p.d)) / BIN) + 1
const hist = computed(() => {
  const rPair = Math.min(R_FMM, rMesh.value)
  const h = Array.from({ length: NB }, () => ({ task: 0, m2l: 0, mesh: 0 }))
  for (const p of pairs) {
    const b = h[Math.floor(p.d / BIN)]
    if (p.d < rPair) b.task += p.n
    else if (p.d < rMesh.value) b.m2l += p.n
    else b.mesh += p.n
  }
  return h
})
const totals = computed(() => hist.value.reduce((t, b) => ({ task: t.task + b.task, m2l: t.m2l + b.m2l }), { task: 0, m2l: 0 }))

// plot geometry (log y)
const PW = 560
const PH = 240
const XMAX = 60 // Mpc shown
const nShow = Math.ceil(XMAX / BIN)
const ymax = Math.log10(Math.max(...hist.value.map((b) => b.task + b.m2l + b.mesh)) * 1.5)
const sx = (d) => (d / XMAX) * PW
const sy = (v) => (v <= 1 ? PH : PH - (Math.log10(v) / ymax) * PH)
const bars = computed(() =>
  hist.value.slice(0, nShow).map((b, i) => {
    const x = sx(i * BIN)
    const w = sx(BIN) - 1
    const tot = b.task + b.m2l + b.mesh
    // stack in log space by fraction of the bar height
    const top = sy(tot)
    const hgt = PH - top
    const f = (v) => (tot ? (v / tot) * hgt : 0)
    return { x, w, top, mesh: f(b.mesh), m2l: f(b.m2l), task: f(b.task) }
  }),
)
const fmt = (n) => (n >= 1e6 ? `${(n / 1e6).toFixed(2)}M` : n >= 1e3 ? `${(n / 1e3).toFixed(1)}k` : `${Math.round(n)}`)
</script>

<template>
  <div class="pth">
    <svg :viewBox="`-50 -10 ${PW + 70} ${PH + 50}`" class="plot">
      <g v-for="(b, i) in bars" :key="i">
        <rect :x="b.x" :y="b.top" :width="b.w" :height="b.mesh" class="mesh" />
        <rect :x="b.x" :y="b.top + b.mesh" :width="b.w" :height="b.m2l" class="m2l" />
        <rect :x="b.x" :y="b.top + b.mesh + b.m2l" :width="b.w" :height="b.task" class="task" />
      </g>
      <line :x1="sx(R_FMM)" :x2="sx(R_FMM)" y1="0" :y2="PH" class="fmm" />
      <text :x="sx(R_FMM) + 4" y="10" class="lbl fmmt">r_FMM</text>
      <line :x1="sx(Math.min(rMesh, XMAX))" :x2="sx(Math.min(rMesh, XMAX))" y1="0" :y2="PH" class="rm" />
      <text :x="sx(Math.min(rMesh, XMAX)) + 4" y="24" class="lbl rmt">r_mesh</text>
      <line x1="0" :x2="PW" :y1="PH" :y2="PH" class="axis" />
      <line x1="0" x2="0" y1="0" :y2="PH" class="axis" />
      <text v-for="t in [0, 10, 20, 30, 40, 50, 60]" :key="t" :x="sx(t)" :y="PH + 14" class="tick">{{ t }}</text>
      <text v-for="e in Math.floor(ymax)" :key="`y${e}`" x="-6" :y="sy(10 ** e) + 3" class="tick yt">10{{ ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷'][e] }}</text>
      <text :x="PW / 2" :y="PH + 32" class="tick">minimum cell separation [Mpc]</text>
      <text x="-40" :y="PH / 2" class="tick" :transform="`rotate(-90 -40 ${PH / 2})`">cell pairs</text>
    </svg>

    <div class="side">
      <label>r_mesh = <b>{{ rMesh.toFixed(1) }} Mpc</b>
        <input v-model.number="logR" type="range" min="-0.5" max="1.5" step="0.005" />
      </label>
      <div class="presets">
        <button v-for="p in PRESETS" :key="p.label" @click="logR = Math.log10(p.r)">{{ p.label }} ({{ p.r }})</button>
      </div>
      <div class="muted small">r_FMM fixed at {{ R_FMM }} Mpc · {{ N }}³ zoom cells of {{ W }} Mpc</div>
      <div class="legend">
        <div><span class="sw task" /> pair tasks <b class="warn">{{ fmt(totals.task) }}</b></div>
        <div><span class="sw m2l" /> multipole only <b>{{ fmt(totals.m2l) }}</b></div>
        <div><span class="sw mesh" /> mesh, no task</div>
      </div>
      <div class="muted small">pair tasks need d &lt; min(r_FMM, r_mesh)</div>
    </div>
  </div>
</template>

<style scoped>
.pth { display: grid; grid-template-columns: 1.7fr 1fr; gap: 20px; align-items: center; font-size: 0.8rem; }
.plot { width: 100%; font-family: var(--mono); }
.mesh { fill: #2a2a2a; }
.m2l { fill: var(--theory); fill-opacity: 0.7; }
.task { fill: var(--warn); }
.fmm { stroke: var(--theory); stroke-dasharray: 4 3; stroke-width: 1.5; }
.rm { stroke: var(--accent); stroke-width: 2; }
.lbl { font-size: 11px; }
.fmmt { fill: var(--theory); }
.rmt { fill: var(--accent); }
.axis { stroke: #777; }
.tick { fill: var(--muted); font-size: 10px; text-anchor: middle; }
.yt { text-anchor: end; }
label { display: block; }
label b { color: var(--accent); }
input[type='range'] { width: 100%; accent-color: var(--accent); }
.presets { display: flex; gap: 6px; flex-wrap: wrap; margin: 4px 0 8px; }
.presets button { font-size: 0.62rem; padding: 1px 8px; border: 1px solid var(--line); border-radius: 999px; color: var(--muted); background: transparent; }
.presets button:hover { border-color: var(--accent); color: var(--accent); }
.legend { margin: 12px 0 6px; line-height: 1.9; }
.sw { display: inline-block; width: 12px; height: 12px; vertical-align: -1px; margin-right: 6px; }
.sw.task { background: var(--warn); }
.sw.m2l { background: var(--theory); opacity: 0.7; }
.sw.mesh { background: #2a2a2a; border: 1px solid #555; }
.small { font-size: 0.65rem; }
</style>
