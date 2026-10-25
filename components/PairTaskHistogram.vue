<script setup>
// Toy model of zoom-cell gravity pairs in a 1 Gpc parent box. The zoom region
// is the geometry from the explorer slide (29^3 background cells, one void
// cell of 34.5 Mpc split to depth 4: 16^3 zoom cells of 2.16 Mpc). Every pair
// of zoom cells is binned by its minimum separation d:
//   d < min(r_FMM, r_mesh)   -> pair task
//   r_FMM <= d < r_mesh      -> multipole (M2L) only
//   d >= r_mesh              -> handled by the mesh, no task at all
// The slider sets the FFT mesh side N; SWIFT's defaults give
//   r_mesh = r_cut_max * a_smooth * L / N = 4.5 * 1.25 * L / N.
// Without a distributed (MPI) FFTW the mesh is capped at N = 1290
// (mesh_gravity.c: N^3 must stay below 2^31).
import { computed, ref } from 'vue'

const L = 1000 // box [Mpc]
const N = 16 // zoom cells per side
const W = 1000 / 29 / 16 // zoom cell width [Mpc]
const R_FMM = 3 * W // fixed, illustrative
const N_MAX_SERIAL = 1290
const LOG_MIN = Math.log2(64)
const LOG_MAX = Math.log2(4096)
const PRESETS = [256, 512, 1024, N_MAX_SERIAL]

const logN = ref(Math.log2(512))
const meshN = computed(() => Math.round(2 ** logN.value))
const rMesh = computed(() => (4.5 * 1.25 * L) / meshN.value)
const needsMPI = computed(() => meshN.value > N_MAX_SERIAL)

// pair counts by integer offset are cheap: count(d) = prod(N - |d_i|)
const pairs = (() => {
  const out = []
  const g = (x) => Math.max(x - 1, 0)
  for (let i = 0; i < N; i++)
    for (let j = 0; j < N; j++)
      for (let k = 0; k < N; k++) {
        if (i + j + k === 0) continue
        const mult = ((i ? 2 : 1) * (j ? 2 : 1) * (k ? 2 : 1)) / 2 // +/- offsets, unordered
        out.push({ d: W * Math.hypot(g(i), g(j), g(k)), n: (N - i) * (N - j) * (N - k) * mult })
      }
  return out
})()

const NPAIRS = (N ** 3 * (N ** 3 - 1)) / 2
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

// histogram (log y)
const PW = 520
const PH = 220
const XMAX = NB * BIN
const ymax = Math.log10(Math.max(...hist.value.map((b) => b.task + b.m2l + b.mesh)) * 1.5)
const sx = (d) => (d / XMAX) * PW
const sy = (v) => (v <= 1 ? PH : PH - (Math.log10(v) / ymax) * PH)
const bars = computed(() =>
  hist.value.map((b, i) => {
    const tot = b.task + b.m2l + b.mesh
    const top = sy(tot)
    const f = (v) => (tot ? (v / tot) * (PH - top) : 0)
    return { x: sx(i * BIN), w: sx(BIN) - 1, top, mesh: f(b.mesh), m2l: f(b.m2l), task: f(b.task) }
  }),
)

// geometry panel: the 16^2 zoom slice, r_mesh and r_FMM around a central cell,
// and one FFT mesh cell for scale
const G = 200
const gs = G / (N * W)
const c = G / 2
const meshCell = computed(() => (L / meshN.value) * gs)

const sliderPct = (n) => `${((Math.log2(n) - LOG_MIN) / (LOG_MAX - LOG_MIN)) * 100}%`
const fmt = (n) => (n >= 1e6 ? `${(n / 1e6).toFixed(2)}M` : n >= 1e3 ? `${(n / 1e3).toFixed(1)}k` : `${Math.round(n)}`)
</script>

<template>
  <div class="pth">
    <div>
      <svg :viewBox="`-50 -10 ${PW + 60} ${PH + 48}`" class="plot">
        <g v-for="(b, i) in bars" :key="i">
          <rect :x="b.x" :y="b.top" :width="b.w" :height="b.mesh" class="mesh" />
          <rect :x="b.x" :y="b.top + b.mesh" :width="b.w" :height="b.m2l" class="m2l" />
          <rect :x="b.x" :y="b.top + b.mesh + b.m2l" :width="b.w" :height="b.task" class="task" />
        </g>
        <line :x1="sx(R_FMM)" :x2="sx(R_FMM)" y1="0" :y2="PH" class="fmm" />
        <text :x="sx(R_FMM) + 4" y="10" class="lbl fmmt">r_FMM</text>
        <line :x1="sx(Math.min(rMesh, XMAX))" :x2="sx(Math.min(rMesh, XMAX))" y1="0" :y2="PH" class="rm" />
        <text :x="sx(Math.min(rMesh, XMAX)) + 4" y="26" class="lbl rmt">r_mesh</text>
        <line x1="0" :x2="PW" :y1="PH" :y2="PH" class="axis" />
        <line x1="0" x2="0" y1="0" :y2="PH" class="axis" />
        <text v-for="t in [0, 10, 20, 30, 40, 50, 60]" :key="t" :x="sx(t)" :y="PH + 14" class="tick">{{ t }}</text>
        <text v-for="e in Math.floor(ymax)" :key="`y${e}`" x="-6" :y="sy(10 ** e) + 3" class="tick yt">10{{ ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷'][e] }}</text>
        <text :x="PW / 2" :y="PH + 32" class="tick">minimum separation of zoom-cell pairs [Mpc]</text>
        <text x="-40" :y="PH / 2" class="tick" :transform="`rotate(-90 -40 ${PH / 2})`">cell pairs</text>
      </svg>
      <div class="legend">
        <span><span class="sw task" /> pair tasks <b class="warn">{{ fmt(totals.task) }}</b></span>
        <span><span class="sw m2l" /> multipole only <b>{{ fmt(totals.m2l) }}</b></span>
        <span><span class="sw mesh" /> mesh, no task</span>
      </div>
    </div>

    <div class="side">
      <svg :viewBox="`0 0 ${G} ${G}`" class="geo">
        <defs>
          <clipPath id="ptclip"><rect :width="G" :height="G" /></clipPath>
        </defs>
        <rect :width="G" :height="G" class="zbg" />
        <g clip-path="url(#ptclip)">
          <line v-for="i in N - 1" :key="`v${i}`" :x1="(i * G) / N" :x2="(i * G) / N" y1="0" :y2="G" class="zl" />
          <line v-for="i in N - 1" :key="`h${i}`" :y1="(i * G) / N" :y2="(i * G) / N" x1="0" :x2="G" class="zl" />
          <circle :cx="c" :cy="c" :r="rMesh * gs" class="rmc" />
          <circle :cx="c" :cy="c" :r="R_FMM * gs" class="fmc" />
        </g>
        <rect :x="c - G / N / 2" :y="c - G / N / 2" :width="G / N" :height="G / N" class="me" />
        <rect :x="G - 6 - meshCell" y="6" :width="meshCell" :height="meshCell" class="mc" />
      </svg>
      <div class="cap">mid-plane slice · <span class="accent">r_mesh</span> · <span class="theory">r_FMM</span> · <span class="warn">□ mesh cell</span></div>
      <div class="setup">
        <div class="muted"># setup (counts are 3D, all {{ fmt(NPAIRS) }} zoom-cell pairs)</div>
        <div>box {{ L }} Mpc · 29³ bkg cells of {{ (L / 29).toFixed(1) }} Mpc</div>
        <div>30 Mpc high-res region · pad 1.1 → 1 void cell</div>
        <div>depth 4 → {{ N }}³ zoom cells of {{ W.toFixed(2) }} Mpc</div>
        <div>r_mesh = 4.5 × 1.25 × L / N<sub>mesh</sub> (SWIFT defaults)</div>
        <div>r_FMM = {{ R_FMM.toFixed(1) }} Mpc (illustrative)</div>
      </div>

      <label class="mt-3">FFT mesh <b :class="{ bad: needsMPI }">{{ meshN }}³</b> <span class="muted">· r_mesh {{ rMesh.toFixed(1) }} Mpc</span></label>
      <div class="rslider">
        <div class="mpi" :style="{ left: sliderPct(N_MAX_SERIAL) }" />
        <input v-model.number="logN" type="range" :min="LOG_MIN" :max="LOG_MAX" step="0.01" />
        <span class="mark" :style="{ left: sliderPct(N_MAX_SERIAL) }">▲ 1290: limit without MPI FFTW</span>
      </div>
      <div class="presets">
        <button v-for="p in PRESETS" :key="p" @click="logN = Math.log2(p)">{{ p }}</button>
      </div>
      <div v-if="needsMPI" class="small bad">N³ > 2³¹: needs a distributed (MPI) FFT</div>
    </div>
  </div>
</template>

<style scoped>
.pth { display: grid; grid-template-columns: 1.55fr 1fr; gap: 24px; align-items: center; font-size: 0.78rem; }
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
.legend { display: flex; gap: 18px; justify-content: center; margin-top: 4px; }
.sw { display: inline-block; width: 11px; height: 11px; vertical-align: -1px; margin-right: 5px; }
.sw.task { background: var(--warn); }
.sw.m2l { background: var(--theory); opacity: 0.7; }
.sw.mesh { background: #2a2a2a; border: 1px solid #555; }
.geo { width: 56%; display: block; margin: 0 auto; border: 1px solid var(--line); }
.zbg { fill: #0a0a0a; }
.zl { stroke: #2f2f2f; stroke-width: 0.6; }
.rmc { fill: color-mix(in srgb, var(--accent) 12%, transparent); stroke: var(--accent); stroke-width: 1.5; }
.fmc { fill: none; stroke: var(--theory); stroke-dasharray: 3 2; stroke-width: 1.2; }
.me { fill: #fff; }
.mc { fill: none; stroke: var(--warn); stroke-width: 1.5; }
.cap { font-size: 0.6rem; color: var(--ink); text-align: center; margin-top: 4px; }
label { display: block; }
label b { color: var(--accent); }
label b.bad { color: var(--bad); }
.rslider { position: relative; padding-bottom: 20px; }
.mpi { position: absolute; top: 3px; right: 0; height: 14px; background: color-mix(in srgb, var(--bad) 45%, transparent); border-radius: 4px; border-left: 2px solid var(--bad); }
input[type='range'] { position: relative; width: 100%; accent-color: var(--accent); }
.mark { position: absolute; top: 20px; transform: translateX(-50%); font-size: 0.58rem; color: var(--bad); white-space: nowrap; }
.presets { display: flex; gap: 6px; margin: 4px 0 6px; }
.presets button { font-size: 0.62rem; padding: 1px 8px; border: 1px solid var(--line); border-radius: 999px; color: var(--muted); background: transparent; }
.presets button:hover { border-color: var(--accent); color: var(--accent); }
.small { font-size: 0.62rem; }
.bad { color: var(--bad); }
</style>

<style scoped>
.setup { margin-top: 6px; border: 1px solid var(--line); border-radius: 6px; padding: 5px 8px; background: #0a0a0a; font-size: 0.6rem; line-height: 1.5; }
</style>
