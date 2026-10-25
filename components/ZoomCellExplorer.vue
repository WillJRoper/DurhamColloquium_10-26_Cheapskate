<script setup>
// SWIFT zoom top-level geometry, following src/zoom_region/zoom_init.c
// (zoom_region_init) one axis at a time:
//   max_dim   = particle extent * region_pad_factor
//   bkg cdim  = bkg_top_level_cells, or auto (zoom_optimise_bkg_cells):
//               floor(L / max_dim), forced odd, -2 if the padded region
//               straddles a cell edge, minimum 8
//   void      = the background cells covering the padded region, centred in
//               the box (zoom_get_void_geometry)
//   zoom      = the zoom region *is* the void region; its cells are the void
//               cells split zoom_top_level_depth times (zoom_get_geometry)
//   pad       = achieved pad factor = zoom dim / particle extent
import { computed, ref } from 'vue'

const L = 1000 // box side [Mpc]
const auto = ref(false)
const userCdim = ref(64)
const depth = ref(2)
const pad = ref(1.1)

const ext = computed(() => 30) // high-res particle extent [Mpc], fixed
const maxDim = computed(() => ext.value * pad.value)

const bkgCdim = computed(() => {
  if (!auto.value) return userCdim.value
  let c = Math.floor(L / maxDim.value)
  if (c % 2 === 0) c--
  const w = L / c
  if (Math.floor((L / 2 - maxDim.value / 2) / w) !== Math.floor((L / 2 + maxDim.value / 2) / w)) c -= 2
  return Math.max(c, 8)
})
const w = computed(() => L / bkgCdim.value)
const voidLo = computed(() => Math.floor((L / 2 - maxDim.value / 2) / w.value))
const voidHi = computed(() => Math.floor((L / 2 + maxDim.value / 2) / w.value))
const nVoid = computed(() => voidHi.value - voidLo.value + 1)
const zoomDim = computed(() => nVoid.value * w.value)
const zoomCdim = computed(() => nVoid.value * 2 ** depth.value)
const zoomW = computed(() => w.value / 2 ** depth.value)
const achievedPad = computed(() => zoomDim.value / ext.value)
const nRegions = computed(() => Math.ceil(zoomDim.value / maxDim.value))

const status = computed(() => {
  if (nRegions.value >= 64) return { cls: 'bad', msg: `error: ${nRegions.value} zoom regions fit in the void: increase bkg_top_level_cells` }
  if (nRegions.value >= 16) return { cls: 'warn', msg: `warning: background cells large vs the zoom region (${nRegions.value} regions fit in the void)` }
  if (achievedPad.value / pad.value >= 2) return { cls: 'warn', msg: `warning: pad region ${Math.floor(achievedPad.value / pad.value)}× larger than requested` }
  return { cls: 'accent', msg: 'ok' }
})

// left panel: the background cells around the void (void +- 2 cells)
const S = 300
const CROP = computed(() => nVoid.value + 4)
const sc = computed(() => S / (CROP.value * w.value))
const cropLo = computed(() => (voidLo.value - 2) * w.value)
const toL = (x) => (x - cropLo.value) * sc.value
const bkgLines = computed(() => Array.from({ length: CROP.value + 1 }, (_, i) => (i * S) / CROP.value))

// full-box panel: every background cell, the void, and the cropped area
const fsc = S / L
const fullLines = computed(() => Array.from({ length: bkgCdim.value + 1 }, (_, i) => i * w.value * fsc))

// right panel: the zoom region (= void) with its zoom cells
const zsc = computed(() => S / zoomDim.value)
const zoomLines = computed(() => (zoomCdim.value > 128 ? [] : Array.from({ length: zoomCdim.value - 1 }, (_, i) => ((i + 1) * S) / zoomCdim.value)))
const voidLines = computed(() => Array.from({ length: nVoid.value - 1 }, (_, i) => ((i + 1) * S) / nVoid.value))
const zLo = computed(() => voidLo.value * w.value)
// a centred square of side `size`, in a panel with scale s and origin lo
const sq = (size, s, lo) => ({ x: (L / 2 - size / 2 - lo) * s, y: (L / 2 - size / 2 - lo) * s, width: size * s, height: size * s })

const fmt = (n) => (n >= 1e6 ? `${(n / 1e6).toFixed(1)}M` : n >= 1e4 ? `${(n / 1e3).toFixed(0)}k` : Math.round(n).toLocaleString())
const fmtL = (x) => (x >= 10 ? x.toFixed(0) : x >= 1 ? x.toFixed(1) : x.toFixed(2))
</script>

<template>
  <div class="zce">
    <div class="panels">
      <div>
        <svg :viewBox="`0 0 ${S} ${S}`" class="panel">
          <rect :width="S" :height="S" class="frame" />
          <line v-for="x in fullLines" :key="`fv${x}`" :x1="x" :x2="x" y1="0" :y2="S" class="bkg thin" />
          <line v-for="x in fullLines" :key="`fh${x}`" :y1="x" :y2="x" x1="0" :x2="S" class="bkg thin" />
          <rect :x="zLo * fsc" :y="zLo * fsc" :width="Math.max(zoomDim * fsc, 2)" :height="Math.max(zoomDim * fsc, 2)" class="void" />
          <rect :x="cropLo * fsc" :y="cropLo * fsc" :width="CROP * w * fsc" :height="CROP * w * fsc" class="inset" />
        </svg>
        <div class="cap">full {{ L }} Mpc box · {{ bkgCdim }}² slice</div>
      </div>
      <div>
        <svg :viewBox="`0 0 ${S} ${S}`" class="panel">
          <rect :width="S" :height="S" class="frame" />
          <rect :x="toL(zLo)" :y="toL(zLo)" :width="zoomDim * sc" :height="zoomDim * sc" class="void" />
          <line v-for="x in bkgLines" :key="`v${x}`" :x1="x" :x2="x" y1="0" :y2="S" class="bkg" />
          <line v-for="x in bkgLines" :key="`h${x}`" :y1="x" :y2="x" x1="0" :x2="S" class="bkg" />
          <rect v-bind="sq(maxDim, sc, cropLo)" class="pad" />
          <rect v-bind="sq(ext, sc, cropLo)" class="region" />
          <rect :width="S" :height="S" class="inset-frame" />
        </svg>
        <div class="cap"><span class="muted">bkg</span> · <span class="warn">void</span> · <span class="theory">high-res</span> · padded</div>
      </div>
      <div>
        <svg :viewBox="`0 0 ${S} ${S}`" class="panel">
          <rect :width="S" :height="S" class="frame void-bg" />
          <line v-for="x in zoomLines" :key="`zv${x}`" :x1="x" :x2="x" y1="0" :y2="S" class="zoom" />
          <line v-for="x in zoomLines" :key="`zh${x}`" :y1="x" :y2="x" x1="0" :x2="S" class="zoom" />
          <line v-for="x in voidLines" :key="`vv${x}`" :x1="x" :x2="x" y1="0" :y2="S" class="voidline" />
          <line v-for="x in voidLines" :key="`vh${x}`" :y1="x" :y2="x" x1="0" :x2="S" class="voidline" />
          <rect v-bind="sq(maxDim, zsc, zLo)" class="pad" />
          <rect v-bind="sq(ext, zsc, zLo)" class="region" />
        </svg>
        <div class="cap">zoom region = void · <span class="accent">zoom cells</span>{{ zoomCdim > 128 ? ' (too many to draw)' : '' }}</div>
      </div>
    </div>

    <div class="side">
      <div class="yaml">
        <div class="muted">ZoomRegion: <span class="text-xs"># high-res particles span 30 Mpc</span></div>
        <label>bkg_top_level_cells: <b>{{ auto ? `auto → ${bkgCdim}` : bkgCdim }}</b>
          <span class="tog"><input v-model="auto" type="checkbox" /> auto</span>
          <input v-model.number="userCdim" type="range" min="8" max="128" step="1" :disabled="auto" />
        </label>
        <label>zoom_top_level_depth: <b>{{ depth }}</b><input v-model.number="depth" type="range" min="1" max="6" step="1" /></label>
        <label>region_pad_factor: <b>{{ pad.toFixed(2) }}</b><input v-model.number="pad" type="range" min="1" max="3" step="0.05" /></label>
      </div>
      <div>
      <table>
        <tbody>
          <tr><td>background cells</td><td>{{ fmt(bkgCdim ** 3) }}</td><td class="muted">{{ bkgCdim }}³ · {{ fmtL(w) }} Mpc</td></tr>
          <tr><td>void cells</td><td>{{ fmt(nVoid ** 3) }}</td><td class="muted">{{ nVoid }}³</td></tr>
          <tr><td>zoom cells</td><td>{{ fmt(zoomCdim ** 3) }}</td><td class="muted">{{ zoomCdim }}³ · {{ fmtL(zoomW) }} Mpc</td></tr>
          <tr><td>achieved pad factor</td><td :class="achievedPad / pad >= 2 ? 'warn' : 'accent'">{{ achievedPad.toFixed(2) }}</td><td class="muted">asked {{ pad.toFixed(2) }}</td></tr>
        </tbody>
      </table>
      <div v-if="status.msg !== 'ok'" :class="['status', status.cls]">{{ status.msg }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.zce { display: flex; flex-direction: column; gap: 10px; font-size: 0.78rem; }
.panels { display: grid; grid-template-columns: repeat(3, 15.5rem); gap: 26px; justify-content: center; }
.side { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; align-items: start; }
.panel { width: 100%; display: block; }
.frame { fill: #050505; stroke: #666; stroke-width: 1.5; }
.void-bg { fill: #1a1405; }
.bkg { stroke: #555; stroke-width: 1; }
.bkg.thin { stroke: #333; stroke-width: 0.5; }
.inset { fill: none; stroke: #fff; stroke-width: 1.5; }
.inset-frame { fill: none; stroke: #fff; stroke-width: 3; }
.void { fill: var(--warn); fill-opacity: 0.25; stroke: var(--warn); stroke-width: 2; }
.voidline { stroke: var(--warn); stroke-width: 1.6; }
.zoom { stroke: var(--accent); stroke-width: 0.6; stroke-opacity: 0.8; }
.pad { fill: none; stroke: var(--theory); stroke-dasharray: 4 3; stroke-width: 1.2; }
.region { fill: var(--theory); fill-opacity: 0.3; stroke: var(--theory); stroke-width: 1.5; }
.cap { text-align: center; font-size: 0.62rem; margin-top: 4px; color: var(--ink); }
.yaml { border: 1px solid var(--line); border-radius: 6px; padding: 8px 10px; background: #0a0a0a; }
.yaml label { display: block; margin: 6px 0 0 12px; }
.yaml b { color: var(--warn); }
.tog { float: right; font-size: 0.7rem; color: var(--muted); }
input[type='range'] { width: 100%; accent-color: var(--accent); }
input[type='range']:disabled { opacity: 0.3; }
input[type='checkbox'] { accent-color: var(--accent); }
table { width: 100%; border-collapse: collapse; }
td { padding: 3px 4px; border-bottom: 1px solid var(--grid); }
td:nth-child(2) { text-align: right; font-weight: 700; }
td:nth-child(3) { text-align: right; font-size: 0.7rem; white-space: nowrap; }
.status { margin-top: 8px; font-size: 0.68rem; }
.status.bad { color: var(--bad); }
.status.warn { color: var(--warn); }
</style>
