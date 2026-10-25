<script setup>
// Toy 2D picture of why zooms hurt over MPI. A 32x32 background grid with one
// void cell holding a 16x16 zoom grid. Ranks get equal angular wedges around
// the zoom region, so every rank owns some zoom cells and some background
// next to them. Every pair task between cells on different ranks is a comm:
//   background-background: neighbouring cells
//   zoom-zoom: minimum separation < r_mesh
//   zoom-background: worst case, the big background cells around the void
//     interact with *every* zoom cell (global mesh only); with a zoom mesh
//     only the zoom cells touching them.
// Mesh cut-offs follow the 3.2 Gpc / 30 Mpc test zoom (3.17 Mpc zoom cells).
import { computed, ref } from 'vue'

const NB = 32
const NZ = 16
const VOID = 16 // void cell index (x and y)
const RANKS = [2, 4, 8, 16, 32, 64]
const MODES = {
  global: { label: 'global mesh only', r: 17.6 / 3.17, allBkg: true },
  zoom: { label: '+ zoom mesh', r: 1.7 / 3.17, allBkg: false },
}

const nRanks = ref(8)
const mode = ref('global')

// all cells in zoom-cell units: background cells are NZ wide
const cells = (() => {
  const out = []
  for (let i = 0; i < NB; i++)
    for (let j = 0; j < NB; j++)
      if (!(i === VOID && j === VOID)) out.push({ zoom: false, i, j, x: i * NZ, y: j * NZ, w: NZ })
  for (let i = 0; i < NZ; i++)
    for (let j = 0; j < NZ; j++) out.push({ zoom: true, x: VOID * NZ + i, y: VOID * NZ + j, w: 1 })
  const c = VOID * NZ + NZ / 2
  for (const cell of out) {
    cell.ang = Math.atan2(cell.y + cell.w / 2 - c, cell.x + cell.w / 2 - c) + Math.PI
    cell.edge = !cell.zoom && Math.max(Math.abs(cell.i - VOID), Math.abs(cell.j - VOID)) === 1
  }
  return out
})()

const gap = (a, b) => {
  const dx = Math.max(0, a.x - (b.x + b.w), b.x - (a.x + a.w))
  const dy = Math.max(0, a.y - (b.y + b.w), b.y - (a.y + a.w))
  return Math.hypot(dx, dy)
}

function buildPairs({ r, allBkg }) {
  const out = []
  for (let a = 0; a < cells.length; a++)
    for (let b = a + 1; b < cells.length; b++) {
      const A = cells[a]
      const B = cells[b]
      if (!A.zoom && !B.zoom) {
        if (gap(A, B) === 0) out.push([a, b, 'bb'])
      } else if (A.zoom && B.zoom) {
        if (gap(A, B) < r) out.push([a, b, 'zz'])
      } else {
        const bkg = A.zoom ? B : A
        if (bkg.edge && (allBkg || gap(A, B) < r)) out.push([a, b, 'zb'])
      }
    }
  return out
}
const PAIRS = { global: buildPairs(MODES.global), zoom: buildPairs(MODES.zoom) }

const rankOf = (cell, n) => Math.min(n - 1, Math.floor((cell.ang / (2 * Math.PI)) * n))
function count(m, n) {
  const c = { bb: 0, zb: 0, zz: 0 }
  for (const [a, b, k] of PAIRS[m]) if (rankOf(cells[a], n) !== rankOf(cells[b], n)) c[k]++
  c.tot = c.bb + c.zb + c.zz
  return c
}
const SERIES = Object.fromEntries(Object.keys(MODES).map((m) => [m, RANKS.map((n) => ({ n, ...count(m, n) }))]))
const now = computed(() => count(mode.value, nRanks.value))

// drawing
const S = 260
const sc = S / (NB * NZ)
const zsc = S / NZ
const hue = (cell) => (rankOf(cell, nRanks.value) * 360) / nRanks.value
const bkgCells = cells.filter((c) => !c.zoom)
const zoomCells = cells.filter((c) => c.zoom)

// comms plot (log-log)
const PW = 300
const PH = 170
const ymax = Math.log10(Math.max(...SERIES.global.map((s) => s.tot))) + 0.3
const px = (n) => ((Math.log2(n) - 1) / 5) * PW
const py = (v) => (v < 1 ? PH : PH - (Math.log10(v) / ymax) * PH)
const line = (m) => SERIES[m].map((s) => `${px(s.n)},${py(s.tot)}`).join(' ')
const fmt = (n) => (n >= 1e3 ? `${(n / 1e3).toFixed(1)}k` : `${n}`)
</script>

<template>
  <div class="zcomms">
    <div class="maps">
      <svg :viewBox="`0 0 ${S} ${S}`" class="map">
        <rect v-for="(c, i) in bkgCells" :key="i" :x="c.x * sc" :y="c.y * sc" :width="c.w * sc" :height="c.w * sc" :fill="`hsl(${hue(c)} 55% ${c.edge ? 55 : 30}%)`" stroke="#000" stroke-width="0.4" />
        <rect :x="VOID * NZ * sc" :y="VOID * NZ * sc" :width="NZ * sc" :height="NZ * sc" fill="#fff" />
      </svg>
      <svg :viewBox="`0 0 ${S} ${S}`" class="map">
        <rect v-for="(c, i) in zoomCells" :key="i" :x="(c.x - VOID * NZ) * zsc" :y="(c.y - VOID * NZ) * zsc" :width="zsc" :height="zsc" :fill="`hsl(${hue(c)} 65% 50%)`" stroke="#000" stroke-width="0.8" />
        <circle :cx="S / 2" :cy="S / 2" :r="(MODES[mode].r + 0.5) * zsc" class="range" />
      </svg>
      <div class="cap">32² background, one wedge per rank<br>(bright = touching the void)</div>
      <div class="cap">16² zoom cells in the void<br>○ r<sub>mesh</sub> around a central cell</div>
    </div>

    <div class="side">
      <label>ranks: <b>{{ nRanks }}</b>
        <input :value="Math.log2(nRanks)" type="range" min="1" max="6" step="1" @input="nRanks = 2 ** +$event.target.value" />
      </label>
      <div class="presets">
        <button v-for="(m, k) in MODES" :key="k" :class="{ on: mode === k }" @click="mode = k">{{ m.label }}</button>
      </div>

      <svg :viewBox="`-34 -6 ${PW + 44} ${PH + 34}`" class="plot">
        <line x1="0" :x2="PW" :y1="PH" :y2="PH" class="axis" />
        <line x1="0" x2="0" y1="0" :y2="PH" class="axis" />
        <polyline :points="line('global')" :class="['l', 'g', { dim: mode !== 'global' }]" />
        <polyline :points="line('zoom')" :class="['l', 'z', { dim: mode !== 'zoom' }]" />
        <line :x1="px(nRanks)" :x2="px(nRanks)" y1="0" :y2="PH" class="now" />
        <text v-for="n in RANKS" :key="n" :x="px(n)" :y="PH + 12" class="tick">{{ n }}</text>
        <text v-for="e in Math.floor(ymax)" :key="`y${e}`" x="-4" :y="py(10 ** e) + 3" class="tick yt">10{{ ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶'][e] }}</text>
        <text :x="PW / 2" :y="PH + 26" class="tick">ranks</text>
        <text :x="PW - 4" :y="py(SERIES.global.at(-1).tot) - 6" class="lbl g">global only</text>
        <text :x="PW - 4" :y="py(SERIES.zoom.at(-1).tot) - 6" class="lbl z">+ zoom mesh</text>
      </svg>

      <table>
        <tbody>
          <tr class="zz"><td>zoom–zoom</td><td>{{ fmt(now.zz) }}</td></tr>
          <tr class="zb"><td>zoom–background</td><td>{{ fmt(now.zb) }}</td></tr>
          <tr class="bb"><td>background–background</td><td>{{ fmt(now.bb) }}</td></tr>
          <tr><td>cross-rank pair tasks</td><td>{{ fmt(now.tot) }}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.zcomms { display: grid; grid-template-columns: 1.25fr 1fr; gap: 22px; align-items: start; font-size: 0.75rem; }
.maps { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.map { width: 100%; display: block; border: 1px solid var(--line); }
.cap { font-size: 0.6rem; color: var(--muted); text-align: center; }
.range { fill: none; stroke: #fff; stroke-width: 2; stroke-dasharray: 5 4; }
label { display: block; margin-bottom: 4px; }
label b { color: var(--warn); }
input[type='range'] { width: 100%; accent-color: var(--accent); }
.presets { display: flex; gap: 6px; margin: 2px 0 6px; }
.presets button { font-size: 0.62rem; padding: 1px 8px; border: 1px solid var(--line); border-radius: 999px; color: var(--muted); background: transparent; }
.presets button.on { border-color: var(--accent); color: var(--accent); }
.plot { width: 100%; font-family: var(--mono); }
.axis { stroke: #777; }
.tick { fill: var(--muted); font-size: 9px; text-anchor: middle; }
.yt { text-anchor: end; }
.lbl { font-size: 9px; text-anchor: end; }
.lbl.g { fill: var(--bad); }
.lbl.z { fill: var(--accent); }
.l { fill: none; stroke-width: 2.4; transition: opacity 0.3s; }
.l.g { stroke: var(--bad); }
.l.z { stroke: var(--accent); }
.l.dim { opacity: 0.35; }
.now { stroke: var(--warn); stroke-dasharray: 3 3; }
table { width: 100%; border-collapse: collapse; margin-top: 4px; }
td { padding: 2px 4px; border-bottom: 1px solid var(--grid); }
td:last-child { text-align: right; font-weight: 700; }
tr.zz td { color: var(--warn); }
tr.zb td { color: var(--theory); }
tr.bb td { color: #aaa; }
</style>
