<script setup>
// Why zooms hurt over MPI. Counts come from scripts/zoom_comms.py (3D: a
// 32^3 background grid whose central void cell holds 16^3 zoom cells,
// ranks = equal azimuthal wedges around the zoom region). Every gravity
// pair closer than the gravity distance r and split across two ranks is a
// communication. The map is the mid-plane slice of the same setup, cropped
// to the 5x5 background cells around the void.
import { computed, ref } from 'vue'
import DATA from './zoom_comms.json'

const NZ = 16
const VOID = 16
const ZOOM_MPC = 3.17 // zoom cell width in the 3.2 Gpc / 30 Mpc test zoom
const MARKS = [
  { label: 'zoom mesh', mpc: 1.7 },
  { label: 'global mesh', mpc: 17.6 },
]
const RMAX_MPC = DATA.hist[DATA.ranks[0]].zz.length * DATA.bin * ZOOM_MPC

const nRanks = ref(8)
const rMpc = ref(17.6)
const r = computed(() => rMpc.value / ZOOM_MPC) // in zoom-cell widths

function count(n, rr) {
  const h = DATA.hist[n]
  const upto = Math.min(Math.ceil(rr / DATA.bin), h.zz.length)
  const sum = (a) => a.slice(0, upto).reduce((s, x) => s + x, 0)
  const c = { zz: sum(h.zz), zb: sum(h.zb), bb: sum(h.bb) }
  c.tot = c.zz + c.zb + c.bb
  return c
}
const series = computed(() => DATA.ranks.map((n) => ({ n, ...count(n, r.value) })))
const now = computed(() => count(nRanks.value, r.value))

// --- map: 5x5 background cells around the void, mid-plane slice
const S = 300
const LO = (VOID - 2) * NZ
const sc = S / (5 * NZ)
const C = VOID * NZ + NZ / 2
const rankOf = (x, y, w, n) => {
  const a = Math.atan2(y + w / 2 - C, x + w / 2 - C) + Math.PI
  return Math.min(n - 1, Math.floor((a / (2 * Math.PI)) * n))
}
const hue = (k) => (k * 360) / nRanks.value
const bkg = []
for (let i = VOID - 2; i <= VOID + 2; i++)
  for (let j = VOID - 2; j <= VOID + 2; j++)
    if (!(i === VOID && j === VOID)) bkg.push({ x: i * NZ, y: j * NZ })
const zoom = []
for (let i = 0; i < NZ; i++) for (let j = 0; j < NZ; j++) zoom.push({ x: VOID * NZ + i, y: VOID * NZ + j })
// gap between a background cell and the zoom region (= the void)
const gapToZoom = (b) => {
  const lo = VOID * NZ
  const hi = lo + NZ
  const dx = Math.max(0, lo - (b.x + NZ), b.x - hi)
  const dy = Math.max(0, lo - (b.y + NZ), b.y - hi)
  return Math.hypot(dx, dy)
}
const reach = computed(() => r.value * sc)

// --- comms vs ranks plot (log-log)
const PW = 300
const PH = 150
const YMAX = Math.log10(count(64, 1e9).tot) + 0.2
const px = (n) => ((Math.log2(n) - 1) / 5) * PW
const py = (v) => (v < 1 ? PH : PH - (Math.max(Math.log10(v), 0) / YMAX) * PH)
const line = (k) => series.value.map((s) => `${px(s.n)},${py(s[k])}`).join(' ')
const fmt = (v) => (v >= 1e6 ? `${(v / 1e6).toFixed(2)}M` : v >= 1e3 ? `${(v / 1e3).toFixed(1)}k` : `${v}`)
const sliderPct = (mpc) => `${((mpc - 0.5) / (RMAX_MPC - 0.5)) * 100}%`
</script>

<template>
  <div class="zcomms">
    <div>
      <svg :viewBox="`0 0 ${S} ${S}`" class="map">
        <rect
          v-for="(b, i) in bkg"
          :key="`b${i}`"
          :x="(b.x - LO) * sc"
          :y="(b.y - LO) * sc"
          :width="NZ * sc"
          :height="NZ * sc"
          :fill="`hsl(${hue(rankOf(b.x, b.y, NZ, nRanks))} 60% ${gapToZoom(b) < r ? 45 : 14}%)`"
          stroke="#000"
          stroke-width="1"
        />
        <rect
          v-for="(z, i) in zoom"
          :key="`z${i}`"
          :x="(z.x - LO) * sc"
          :y="(z.y - LO) * sc"
          :width="sc"
          :height="sc"
          :fill="`hsl(${hue(rankOf(z.x, z.y, 1, nRanks))} 70% 55%)`"
          stroke="#000"
          stroke-width="0.3"
        />
        <rect
          :x="2 * NZ * sc - reach"
          :y="2 * NZ * sc - reach"
          :width="NZ * sc + 2 * reach"
          :height="NZ * sc + 2 * reach"
          :rx="reach"
          class="range"
        />
      </svg>
      <div class="cap">mid-plane slice · zoom region + nearest background cells<br>bright background = within r of the zoom region · ⬚ r</div>
    </div>

    <div class="side">
      <label>gravity distance r = <b>{{ rMpc.toFixed(1) }} Mpc</b></label>
      <div class="rslider">
        <input v-model.number="rMpc" type="range" min="0.5" :max="RMAX_MPC.toFixed(1)" step="0.1" />
        <span v-for="m in MARKS" :key="m.label" class="mark" :style="{ left: sliderPct(m.mpc), transform: m.mpc < 5 ? 'none' : 'translateX(-50%)', textAlign: m.mpc < 5 ? 'left' : 'center' }" @click="rMpc = m.mpc">▲<br>{{ m.label }}</span>
      </div>
      <label>ranks: <b>{{ nRanks }}</b></label>
      <input :value="Math.log2(nRanks)" type="range" min="1" max="6" step="1" @input="nRanks = 2 ** +$event.target.value" />

      <svg :viewBox="`-38 -6 ${PW + 48} ${PH + 32}`" class="plot">
        <line x1="0" :x2="PW" :y1="PH" :y2="PH" class="axis" />
        <line x1="0" x2="0" y1="0" :y2="PH" class="axis" />
        <polyline :points="line('bb')" class="l bb" />
        <polyline :points="line('zz')" class="l zz" />
        <polyline :points="line('zb')" class="l zb" />
        <polyline :points="line('tot')" class="l tot" />
        <line :x1="px(nRanks)" :x2="px(nRanks)" y1="0" :y2="PH" class="now" />
        <text v-for="n in DATA.ranks" :key="n" :x="px(n)" :y="PH + 12" class="tick">{{ n }}</text>
        <text v-for="e in Math.floor(YMAX)" :key="`y${e}`" x="-4" :y="py(10 ** e) + 3" class="tick yt">10{{ ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷'][e] }}</text>
        <text :x="PW / 2" :y="PH + 26" class="tick">ranks</text>
      </svg>

      <table>
        <tbody>
          <tr class="zb"><td>background ↔ zoom</td><td>{{ fmt(now.zb) }}</td></tr>
          <tr class="zz"><td>zoom ↔ zoom</td><td>{{ fmt(now.zz) }}</td></tr>
          <tr class="bb"><td>background ↔ background</td><td>{{ fmt(now.bb) }}</td></tr>
          <tr class="tot"><td>cross-rank pairs (3D)</td><td>{{ fmt(now.tot) }}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.zcomms { display: grid; grid-template-columns: 1fr 1.05fr; gap: 28px; align-items: start; font-size: 0.75rem; }
.map { width: 100%; display: block; border: 1px solid var(--line); }
.cap { font-size: 0.6rem; color: var(--muted); text-align: center; margin-top: 4px; }
.range { fill: none; stroke: #fff; stroke-width: 2; stroke-dasharray: 6 4; }
label { display: block; }
label b { color: var(--warn); }
.rslider { overflow: visible; background: none; border: 0; position: relative; padding-bottom: 34px; margin-bottom: 4px; }
input[type='range'] { width: 100%; accent-color: var(--accent); }
.mark { position: absolute; top: 20px; transform: translateX(-50%); font-size: 0.62rem; color: #bbb; z-index: 1; text-align: center; line-height: 1.1; cursor: pointer; white-space: nowrap; }
.mark:hover { color: var(--accent); }
.plot { width: 100%; font-family: var(--mono); margin-top: 6px; }
.axis { stroke: #777; }
.tick { fill: var(--muted); font-size: 9px; text-anchor: middle; }
.yt { text-anchor: end; }
.l { fill: none; stroke-width: 2.2; }
.l.zb { stroke: var(--theory); }
.l.zz { stroke: var(--warn); }
.l.bb { stroke: #888; }
.l.tot { stroke: #fff; stroke-width: 1.4; stroke-dasharray: 4 3; }
.now { stroke: var(--accent); stroke-dasharray: 3 3; }
table { width: 100%; border-collapse: collapse; margin-top: 4px; }
td { padding: 2px 4px; border-bottom: 1px solid var(--grid); }
td:last-child { text-align: right; font-weight: 700; }
tr.zb td { color: var(--theory); }
tr.zz td { color: var(--warn); }
tr.bb td { color: #aaa; }
tr.tot td { color: var(--ink); }
</style>
