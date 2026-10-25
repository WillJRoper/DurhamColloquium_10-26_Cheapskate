<script setup>
// Theory <-> observation flowchart (after Wilkins & Lovell).
// step: 0 nodes, 1 + theory arrows, 2 + inverse arrows.
// highlight: '' | 'sims' | 'forward' dims every arrow outside that group.
const props = defineProps({
  step: { type: Number, default: 2 },
  highlight: { type: String, default: '' },
})

const theory = [
  { group: 'sims', label: ['Numerical', 'simulations'], d: 'M110 160 V115 H290 V158', lx: 200, ly: 85 },
  { group: 'sims', label: ['Structure finding /', 'semi-analytic models'], d: 'M305 160 V115 H455 V158', lx: 380, ly: 85 },
  { group: 'forward', label: ['SED modelling'], d: 'M475 160 V115 H655 V158', lx: 565, ly: 100 },
  { group: 'forward', label: ['SED + image modelling'], d: 'M320 160 V55 H850 V158', lx: 585, ly: 45 },
]
const inverse = [
  { label: ['Phenomenological', 'modelling'], d: 'M455 220 V270 H110 V222', lx: 280, ly: 292 },
  { label: ['SED fitting'], d: 'M655 220 V270 H475 V222', lx: 565, ly: 292 },
  { label: ['Source', 'identification'], d: 'M850 220 V270 H670 V222', lx: 760, ly: 292 },
]
const nodes = [
  { x: 30, w: 160, label: 'Physics' },
  { x: 225, w: 150, label: 'Fields' },
  { x: 410, w: 340, label: 'Galaxies' },
  { x: 785, w: 185, label: 'Observations' },
]
const dim = (g) => props.highlight && g !== props.highlight
</script>

<template>
  <svg viewBox="0 0 1000 330" class="flow">
    <defs>
      <marker id="ah-t" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M0 0 L10 5 L0 10 z" fill="var(--theory)" />
      </marker>
      <marker id="ah-i" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M0 0 L10 5 L0 10 z" fill="var(--accent)" />
      </marker>
    </defs>

    <g v-for="n in nodes" :key="n.label">
      <rect :x="n.x" y="160" :width="n.w" height="60" rx="8" class="node" />
      <text :x="n.x + n.w / 2" y="196" class="node-label">{{ n.label }}</text>
    </g>
    <text x="465" y="185" class="sub">Physical</text>
    <text x="465" y="203" class="sub">properties</text>
    <text x="695" y="185" class="sub">Observable</text>
    <text x="695" y="203" class="sub">properties</text>

    <g :class="['arrows', { show: step >= 1 }]">
      <g v-for="a in theory" :key="a.d" :class="{ dim: dim(a.group), hot: highlight === a.group }">
        <path :d="a.d" class="arrow theory" marker-end="url(#ah-t)" />
        <text v-for="(l, i) in a.label" :key="l" :x="a.lx" :y="a.ly + i * 15" class="lbl theory">{{ l }}</text>
      </g>
    </g>

    <g :class="['arrows', { show: step >= 2 }]">
      <g v-for="a in inverse" :key="a.d" :class="{ dim: !!highlight, hot: highlight === 'inverse' }">
        <path :d="a.d" class="arrow inverse" marker-end="url(#ah-i)" />
        <text v-for="(l, i) in a.label" :key="l" :x="a.lx" :y="a.ly + i * 15" class="lbl inverse">{{ l }}</text>
      </g>
    </g>
  </svg>
</template>

<style scoped>
.flow { width: 100%; overflow: visible; font-family: var(--mono); }
.node { fill: #111; stroke: #555; stroke-width: 1.5; }
.node-label { fill: var(--ink); font-size: 20px; font-weight: 700; text-anchor: middle; }
.sub { fill: var(--muted); font-size: 12px; text-anchor: middle; }
.arrow { fill: none; stroke-width: 2.2; }
.arrow.theory { stroke: var(--theory); }
.arrow.inverse { stroke: var(--accent); }
.lbl { font-size: 15px; text-anchor: middle; }
.lbl.theory { fill: var(--theory); }
.lbl.inverse { fill: var(--accent); }
.arrows { opacity: 0; transition: opacity 0.5s; }
.arrows.show { opacity: 1; }
.arrows g { transition: opacity 0.5s; }
.arrows g.dim { opacity: 0.18; }
.arrows g.hot .arrow { stroke-width: 3.5; stroke-dasharray: 9 6; animation: flow 1s linear infinite; }
.arrows g.hot .lbl { font-weight: 700; }
@keyframes flow { to { stroke-dashoffset: -15; } }
</style>
