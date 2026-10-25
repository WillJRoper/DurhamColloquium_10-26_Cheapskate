<script setup>
// Toy 2D version of SWIFT-zoom top-level cell construction, driven by the
// same knobs as the ZoomRegion parameters: background cells tile the box,
// the background cells overlapping the padded zoom region become "void"
// cells, and each void cell is split zoom_top_level_depth times into zoom cells.
import { computed, ref } from 'vue'

const L = 3200 // box side [Mpc]
const nBkg = ref(63)
const depth = ref(4)
const logR = ref(Math.log10(30))
const pad = ref(1.1)

const R = computed(() => 10 ** logR.value)
const wBkg = computed(() => L / nBkg.value)
// void cells: background cells overlapping the padded region, centred in the box
const voidRange = computed(() => {
  const half = (R.value * pad.value) / 2
  const lo = Math.floor((L / 2 - half) / wBkg.value)
  const hi = Math.ceil((L / 2 + half) / wBkg.value) - 1
  return { lo, hi, n: hi - lo + 1 }
})
const zoomPerVoid = computed(() => 2 ** depth.value)
const nZoomSide = computed(() => voidRange.value.n * zoomPerVoid.value)
const wZoom = computed(() => wBkg.value / zoomPerVoid.value)
// zoom cells actually touching the (unpadded) high-res region
const usefulSide = computed(() => {
  const x0 = voidRange.value.lo * wBkg.value
  const lo = Math.floor((L / 2 - R.value / 2 - x0) / wZoom.value)
  const hi = Math.ceil((L / 2 + R.value / 2 - x0) / wZoom.value) - 1
  return Math.max(1, hi - lo + 1)
})
const useful = computed(() => (usefulSide.value / nZoomSide.value) ** 3)

// right panel: the void block, scaled to fit
const VB = 300
const voidSize = computed(() => voidRange.value.n * wBkg.value)
const toVoid = (x) => (x / voidSize.value) * VB
const regionPx = computed(() => toVoid(R.value))
const padPx = computed(() => toVoid(R.value * pad.value))
const zoomLines = computed(() => {
  const n = nZoomSide.value
  return n > 128 ? [] : Array.from({ length: n - 1 }, (_, i) => ((i + 1) / n) * VB)
})
const voidLines = computed(() => Array.from({ length: voidRange.value.n - 1 }, (_, i) => ((i + 1) / voidRange.value.n) * VB))

// left panel: whole box
const BB = 300
const bkgLines = computed(() => (nBkg.value > 96 ? [] : Array.from({ length: nBkg.value - 1 }, (_, i) => ((i + 1) / nBkg.value) * BB)))
const voidBox = computed(() => ({
  x: (voidRange.value.lo / nBkg.value) * BB,
  w: Math.max((voidRange.value.n / nBkg.value) * BB, 2),
}))

const fmt = (n) => (n >= 1e6 ? `${(n / 1e6).toFixed(1)}M` : n >= 1e4 ? `${(n / 1e3).toFixed(0)}k` : Math.round(n).toLocaleString())
const fmtL = (x) => (x >= 10 ? x.toFixed(0) : x >= 1 ? x.toFixed(1) : x.toFixed(2))
</script>

<template>
  <div class="zce">
    <div class="panels">
      <div>
        <svg :viewBox="`0 0 ${BB} ${BB}`" class="panel">
          <rect :width="BB" :height="BB" class="frame" />
          <line v-for="x in bkgLines" :key="`v${x}`" :x1="x" :x2="x" y1="0" :y2="BB" class="bkg" />
          <line v-for="x in bkgLines" :key="`h${x}`" :y1="x" :y2="x" x1="0" :x2="BB" class="bkg" />
          <rect :x="voidBox.x" :y="voidBox.x" :width="voidBox.w" :height="voidBox.w" class="void" />
        </svg>
        <div class="cap">{{ L }} Mpc box · <span class="muted">background</span> + <span class="warn">void</span></div>
      </div>
      <div>
        <svg :viewBox="`0 0 ${VB} ${VB}`" class="panel">
          <rect :width="VB" :height="VB" class="frame void-bg" />
          <line v-for="x in zoomLines" :key="`zv${x}`" :x1="x" :x2="x" y1="0" :y2="VB" class="zoom" />
          <line v-for="x in zoomLines" :key="`zh${x}`" :y1="x" :y2="x" x1="0" :x2="VB" class="zoom" />
          <line v-for="x in voidLines" :key="`vv${x}`" :x1="x" :x2="x" y1="0" :y2="VB" class="voidline" />
          <line v-for="x in voidLines" :key="`vh${x}`" :y1="x" :y2="x" x1="0" :x2="VB" class="voidline" />
          <rect :x="(VB - padPx) / 2" :y="(VB - padPx) / 2" :width="padPx" :height="padPx" class="pad" />
          <rect :x="(VB - regionPx) / 2" :y="(VB - regionPx) / 2" :width="regionPx" :height="regionPx" class="region" />
        </svg>
        <div class="cap">void region · <span class="accent">zoom cells</span> · <span class="theory">high-res region</span></div>
      </div>
    </div>

    <div class="side">
      <div class="yaml">
        <div class="muted">ZoomRegion:</div>
        <label>bkg_top_level_cells: <b>{{ nBkg }}</b><input v-model.number="nBkg" type="range" min="4" max="128" step="1" /></label>
        <label>zoom_top_level_depth: <b>{{ depth }}</b><input v-model.number="depth" type="range" min="0" max="6" step="1" /></label>
        <label>region_pad_factor: <b>{{ pad.toFixed(2) }}</b><input v-model.number="pad" type="range" min="1" max="3" step="0.05" /></label>
        <label>high-res region: <b>{{ fmtL(R) }} Mpc</b><input v-model.number="logR" type="range" min="0.7" max="2.7" step="0.01" /></label>
      </div>
      <table>
        <tbody>
        <tr><td>background cells</td><td>{{ fmt(nBkg ** 3 - voidRange.n ** 3) }}</td><td class="muted">{{ fmtL(wBkg) }} Mpc</td></tr>
        <tr><td>void cells</td><td>{{ fmt(voidRange.n ** 3) }}</td><td class="muted">{{ voidRange.n }}³</td></tr>
        <tr><td>zoom cells</td><td>{{ fmt(nZoomSide ** 3) }}</td><td class="muted">{{ fmtL(wZoom) }} Mpc</td></tr>
        <tr><td>zoom cells holding high-res particles</td><td :class="useful < 0.3 ? 'bad' : 'accent'">{{ (useful * 100).toFixed(0) }}%</td><td /></tr>
      </tbody>
      </table>
      <div class="muted note">counts in 3D; drawn as a 2D slice</div>
    </div>
  </div>
</template>

<style scoped>
.zce { display: grid; grid-template-columns: 1fr 0.95fr; gap: 24px; align-items: start; font-size: 0.8rem; }
.panels { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.panel { width: 100%; display: block; }
.frame { fill: #050505; stroke: #666; stroke-width: 1.5; }
.void-bg { fill: #1a1405; }
.bkg { stroke: #3a3a3a; stroke-width: 0.6; }
.void { fill: var(--warn); fill-opacity: 0.5; stroke: var(--warn); stroke-width: 1.5; }
.voidline { stroke: var(--warn); stroke-width: 1.4; }
.zoom { stroke: var(--accent); stroke-width: 0.5; stroke-opacity: 0.7; }
.pad { fill: none; stroke: var(--theory); stroke-dasharray: 4 3; stroke-width: 1; }
.region { fill: var(--theory); fill-opacity: 0.25; stroke: var(--theory); stroke-width: 1.5; }
.cap { text-align: center; font-size: 0.65rem; margin-top: 4px; color: var(--ink); }
.yaml { border: 1px solid var(--line); border-radius: 6px; padding: 8px 10px; background: #0a0a0a; }
.yaml label { display: block; margin: 6px 0 0 12px; }
.yaml b { color: var(--warn); }
input[type='range'] { width: 100%; accent-color: var(--accent); }
table { width: 100%; margin-top: 10px; border-collapse: collapse; }
td { padding: 3px 4px; border-bottom: 1px solid var(--grid); }
td:nth-child(2) { text-align: right; font-weight: 700; }
td:nth-child(3) { text-align: right; font-size: 0.7rem; white-space: nowrap; }
.bad { color: var(--bad); }
.note { font-size: 0.6rem; margin-top: 4px; }
</style>
