<script setup>
// The PacmanEmission model tree (15 models), walked through one model at a
// time, then varied with ParameterLists. Structure and variant counts follow
// the Synthesizer docs (emission_models/model_variations): models upstream of
// a varied parameter are shared, everything downstream is duplicated.
import { computed, ref, watch } from 'vue'

const props = defineProps({ step: { type: Number, default: 0 } })

const KIND = {
  extraction: { colour: 'var(--theory)', label: 'Extraction' },
  transformation: { colour: 'var(--warn)', label: 'Transformation' },
  combination: { colour: 'var(--accent)', label: 'Combination' },
  generation: { colour: '#f472b6', label: 'Generation' },
}

// x, y in a 900 x 600 frame; deps: f = fesc, t = tau_v
const NODES = {
  incident: { x: 113, y: 560, kind: 'extraction', deps: '', what: 'Pure stellar emission from the SPS grid.', code: `IncidentEmission(grid)\n# extract="incident"` },
  full_transmitted: { x: 320, y: 560, kind: 'extraction', deps: '', what: 'Starlight after passing through the birth cloud (from Cloudy).', code: `extract="transmitted"` },
  _nebular_line_no_fesc: { x: 550, y: 560, kind: 'extraction', deps: '', what: 'Nebular line emission from the photoionised gas.', code: `extract="linecont"` },
  nebular_continuum: { x: 780, y: 560, kind: 'extraction', deps: '', what: 'Nebular continuum emission from the photoionised gas.', code: `extract="nebular_continuum"` },
  escaped: { x: 113, y: 470, kind: 'transformation', deps: 'f', from: ['incident'], what: 'The fraction of starlight that escapes without being reprocessed.', code: `transformer=EscapedFraction()\napply_to=incident\nfesc=0.2` },
  transmitted: { x: 320, y: 470, kind: 'transformation', deps: 'f', from: ['full_transmitted'], what: 'The fraction that does get processed by the gas.', code: `transformer=ProcessedFraction()\napply_to=full_transmitted\nfesc=0.2` },
  nebular_line: { x: 550, y: 470, kind: 'transformation', deps: '', from: ['_nebular_line_no_fesc'], what: 'Line emission with a separate Lyman-α escape fraction.', code: `transformer=EscapedFraction()\nfesc_ly_alpha=0.9` },
  nebular_combined: { x: 666, y: 390, kind: 'combination', deps: '', from: ['nebular_line', 'nebular_continuum'], what: 'Lines + continuum.', code: `combine=(nebular_line,\n         nebular_continuum)` },
  nebular: { x: 666, y: 310, kind: 'transformation', deps: 'f', from: ['nebular_combined'], also: ['_nebular_line_no_fesc', 'nebular_line', 'nebular_continuum'], what: 'Emission from the gas the stars photoionise: lines (with their own Lyman-α escape) plus the nebular continuum, both from Cloudy. Only the processed fraction (1 − fesc) produces it.', code: `# lines\nextract="linecont"\nfesc_ly_alpha=0.9\n# continuum\nextract="nebular_continuum"\n# lines + continuum, then\ntransformer=ProcessedFraction()\nfesc=0.2` },
  reprocessed: { x: 470, y: 235, kind: 'combination', deps: 'f', from: ['transmitted', 'nebular'], what: 'Everything that went through the gas.', code: `combine=(transmitted, nebular)` },
  intrinsic: { x: 182, y: 160, kind: 'combination', deps: 'f', from: ['reprocessed', 'escaped'], what: 'All the light before any dust.', code: `combine=(reprocessed, escaped)` },
  attenuated: { x: 470, y: 160, kind: 'transformation', deps: 'ft', from: ['reprocessed'], what: 'Reprocessed light through a dust screen.', code: `dust_curve=PowerLaw(slope=-1.3)\napply_to=reprocessed\ntau_v=0.7` },
  emergent: { x: 470, y: 90, kind: 'combination', deps: 'ft', from: ['attenuated', 'escaped'], what: 'What leaves the galaxy in the UV–NIR.', code: `combine=(attenuated, escaped)` },
  dust_emission: { x: 792, y: 90, kind: 'generation', deps: 'ft', from: ['intrinsic', 'emergent'], what: 'Energy balance: what the dust absorbed comes back out in the IR.', code: `generator=Greybody(\n  temperature=30 * K,\n  emissivity=2.0)\nlum_intrinsic_model=intrinsic\nlum_attenuated_model=emergent` },
  total: { x: 631, y: 20, kind: 'combination', deps: 'ft', from: ['emergent', 'dust_emission'], what: 'The full SED.', code: `combine=(emergent, dust_emission)` },
}
const W = 180
const H = 38

// walk-through order, one model per click
const TOUR = ['incident', 'full_transmitted', 'escaped', 'transmitted', 'nebular', 'reprocessed', 'attenuated', 'emergent', 'dust_emission', 'total']
const VARY_STEP = TOUR.length + 1

const picked = ref(null)
watch(() => props.step, () => (picked.value = null))
const varying = computed(() => props.step >= VARY_STEP)
const selected = computed(() => picked.value ?? (props.step >= 1 && props.step <= TOUR.length ? TOUR[props.step - 1] : null))

const nf = ref(2)
const nt = ref(3)
const lin = (a, b, n) => (n === 1 ? [a] : Array.from({ length: n }, (_, i) => +(a + ((b - a) * i) / (n - 1)).toFixed(2)))
const fescs = computed(() => lin(0, 0.5, nf.value))
const taus = computed(() => lin(0.1, 1.5, nt.value))

const copies = (name) => {
  if (!varying.value) return 1
  const d = NODES[name].deps
  return (d.includes('f') ? nf.value : 1) * (d.includes('t') ? nt.value : 1)
}
const total = computed(() => Object.keys(NODES).reduce((s, k) => s + copies(k), 0))
const naive = computed(() => Object.keys(NODES).length * nf.value * nt.value)

const edges = Object.entries(NODES).flatMap(([to, n]) => (n.from || []).map((from) => ({ from, to })))
const edgePath = ({ from, to }) => {
  const a = NODES[from]
  const b = NODES[to]
  const my = (a.y + b.y + H) / 2
  return `M ${a.x} ${a.y} C ${a.x} ${my}, ${b.x} ${my}, ${b.x} ${b.y + H}`
}
const lit = (name) => {
  const s = selected.value
  if (!s) return true
  return name === s || (NODES[s].from || []).includes(name) || (NODES[s].also || []).includes(name)
}
const stackN = (name) => Math.min(copies(name), 8)
</script>

<template>
  <div class="emx">
    <svg viewBox="-10 -40 1010 650" class="tree">
      <path v-for="e in edges" :key="e.from + e.to" :d="edgePath(e)" :class="['edge', { on: selected && (e.to === selected || (lit(e.to) && lit(e.from))) }]" />
      <g v-for="(n, name) in NODES" :key="name" :class="['node', { dim: !lit(name), sel: name === selected }]" @click="picked = name">
        <rect
          v-for="k in stackN(name) - 1"
          :key="k"
          :x="n.x - W / 2 + 7 * (stackN(name) - k)"
          :y="n.y - 7 * (stackN(name) - k)"
          :width="W"
          :height="H"
          rx="6"
          class="ghost"
          :style="{ stroke: KIND[n.kind].colour }"
        />
        <rect :x="n.x - W / 2" :y="n.y" :width="W" :height="H" rx="6" class="box" :style="{ stroke: KIND[n.kind].colour }" />
        <text :x="n.x" :y="n.y + H / 2 + 5" class="lbl">{{ name }}</text>
        <g v-if="copies(name) > 1">
          <circle :cx="n.x + W / 2 + 10" :cy="n.y - 6" r="17" class="badge" />
          <text :x="n.x + W / 2 + 10" :y="n.y - 1" class="badge-t">×{{ copies(name) }}</text>
        </g>
      </g>
    </svg>

    <div class="panel">
      <template v-if="varying">
        <div class="head accent">Varying a model</div>
        <label>fesc: <b>{{ nf }}</b> value{{ nf > 1 ? 's' : '' }}<input v-model.number="nf" type="range" min="1" max="8" /></label>
        <label>tau_v: <b>{{ nt }}</b> value{{ nt > 1 ? 's' : '' }}<input v-model.number="nt" type="range" min="1" max="8" /></label>
        <pre class="code">PacmanEmission(
  grid,
  fesc=ParameterList(
    {{ JSON.stringify(fescs) }}),
  tau_v=ParameterList(
    {{ JSON.stringify(taus) }}),
  ...
).expand_models()</pre>
        <table>
          <tbody>
            <tr><td>combinations</td><td>{{ nf * nt }}</td></tr>
            <tr><td>models, one per combination</td><td class="bad">{{ naive }}</td></tr>
            <tr><td>models after expand_models()</td><td class="accent">{{ total }}</td></tr>
          </tbody>
        </table>
        <div class="muted small">Only what depends on a varied parameter is duplicated. Grid extractions happen once, and it's all one get_spectra call.</div>
      </template>
      <template v-else-if="selected">
        <div class="head" :style="{ color: KIND[NODES[selected].kind].colour }">{{ KIND[NODES[selected].kind].label }}</div>
        <div class="name">{{ selected }}</div>
        <div class="what">{{ NODES[selected].what }}</div>
        <pre class="code">{{ NODES[selected].code }}</pre>
      </template>
      <template v-else>
        <div class="head">PacmanEmission</div>
        <div class="what">One model object, 15 linked models.</div>
        <div class="legend">
          <div v-for="(k, key) in KIND" :key="key"><span class="sw" :style="{ borderColor: k.colour }" /> {{ k.label }}</div>
        </div>
        <pre class="code">PacmanEmission(
  grid,
  tau_v=0.7,
  dust_curve=PowerLaw(slope=-1.3),
  dust_emission=Greybody(30*K, 2),
  fesc=0.2,
  fesc_ly_alpha=0.9,
)</pre>
      </template>
    </div>
  </div>
</template>

<style scoped>
.emx { display: grid; grid-template-columns: 1.9fr 1fr; gap: 20px; align-items: center; font-size: 0.8rem; }
.tree { width: 100%; font-family: var(--mono); }
.edge { fill: none; stroke: #444; stroke-width: 1.5; transition: stroke 0.3s; }
.edge.on { stroke: #ddd; stroke-width: 2.5; }
.node { cursor: pointer; transition: opacity 0.3s; }
.node.dim { opacity: 0.25; }
.box { fill: #0d0d0d; stroke-width: 2; }
.node.sel .box { fill: #1d1d1d; stroke-width: 3.5; }
.ghost { fill: #0d0d0d; stroke-width: 1.2; opacity: 0.7; }
.lbl { fill: var(--ink); font-size: 14px; text-anchor: middle; }
.badge { fill: var(--bad); }
.badge-t { fill: #000; font-size: 14px; font-weight: 700; text-anchor: middle; }
.panel { border: 1px solid var(--line); border-radius: 8px; background: #0a0a0a; padding: 12px 14px; min-height: 22rem; }
.head { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--muted); margin-bottom: 4px; }
.name { font-size: 1.15rem; font-weight: 700; margin-bottom: 6px; }
.what { margin-bottom: 10px; }
.code { font-family: var(--mono); font-size: 0.72rem; background: #000; border: 1px solid var(--grid); border-radius: 6px; padding: 8px 10px; color: var(--theory); white-space: pre-wrap; margin: 8px 0; }
.legend { line-height: 1.9; margin: 8px 0; }
.sw { display: inline-block; width: 14px; height: 10px; border: 2px solid; border-radius: 3px; margin-right: 6px; vertical-align: -1px; }
label { display: block; margin: 4px 0; }
label b { color: var(--warn); }
input[type='range'] { width: 100%; accent-color: var(--accent); }
table { width: 100%; border-collapse: collapse; margin: 6px 0; }
td { padding: 3px 4px; border-bottom: 1px solid var(--grid); }
td:last-child { text-align: right; font-weight: 700; }
.bad { color: var(--bad); }
.small { font-size: 0.65rem; }
</style>
