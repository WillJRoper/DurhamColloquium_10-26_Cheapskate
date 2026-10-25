<script setup>
// Back-of-the-envelope Pipeline cost, calibrated on the Synthesizer docs
// benchmarks (COSMA8, 2 x AMD EPYC 7763):
//   per-galaxy time vs star particles: Pipeline profiling, 10 galaxies,
//     PacmanEmission + dust, 8 NIRCam filters, lines, images (rest + obs),
//     32 threads -> TOTAL read off the plot below (seconds for 10 galaxies).
//   threads: integrated-spectra thread scaling, ~12x on 32 threads
//     -> Amdahl with a parallel fraction of 0.95.
//   ranks: MPI strong scaling, ~97% efficient at 32 ranks.
// Galaxies are drawn from a z ~ 0 Schechter GSMF (log M* = 10.7,
// alpha = -1.3) between 100 star particles and 10^12 Msun, so the mean
// particle count per galaxy follows from the stellar particle mass.
import { computed, ref } from 'vue'

const BENCH = [ // [particles, seconds for 10 galaxies at 32 threads]
  [100, 1.2], [500, 1.45], [1000, 1.55], [5000, 3.1], [1e4, 5.3], [1e5, 38],
]
const F_PAR = 0.95
const speedup = (p) => 1 / (1 - F_PAR + F_PAR / p)
const EFF_MPI = 0.97

function tGal32(n) { // seconds per galaxy at 32 threads, log-log interpolation
  const x = Math.log10(Math.max(n, BENCH[0][0]))
  for (let i = 1; i < BENCH.length; i++) {
    const [n0, t0] = BENCH[i - 1]
    const [n1, t1] = BENCH[i]
    if (x <= Math.log10(n1)) {
      const f = (x - Math.log10(n0)) / (Math.log10(n1) - Math.log10(n0))
      return 10 ** (Math.log10(t0) + f * (Math.log10(t1) - Math.log10(t0))) / 10
    }
  }
  const [nl, tl] = BENCH.at(-1)
  return (tl * (n / nl)) / 10 // linear beyond the last point
}

// mean stellar mass of a Schechter population between mLo and mHi
const LOGMSTAR = 10.7
const ALPHA = -1.3
function meanMass(mLo, mHi) {
  let num = 0
  let den = 0
  for (let lm = Math.log10(mLo); lm < Math.log10(mHi); lm += 0.01) {
    const x = 10 ** (lm - LOGMSTAR)
    const w = x ** (ALPHA + 1) * Math.exp(-x)
    num += w * 10 ** lm
    den += w
  }
  return den ? num / den : mLo
}

const logNgal = ref(2)
const logMpart = ref(6)
const threads = ref(16)
const logRanks = ref(0)

const nGal = computed(() => Math.round(10 ** logNgal.value))
const mPart = computed(() => 10 ** logMpart.value)
const ranks = computed(() => 2 ** logRanks.value)
const mLo = computed(() => 100 * mPart.value)
const nMean = computed(() => (mLo.value >= 1e12 ? 100 : meanMass(mLo.value, 1e12) / mPart.value))
const tGal = computed(() => (tGal32(nMean.value) * speedup(32)) / speedup(threads.value))
const wall = computed(() => (Math.ceil(nGal.value / ranks.value) * tGal.value) / (ranks.value > 1 ? EFF_MPI : 1))
const cpuHours = computed(() => (wall.value * ranks.value * threads.value) / 3600)

function human(s) {
  for (const [d, u] of [[3.156e7, 'yr'], [86400, 'days'], [3600, 'hr'], [60, 'min'], [1, 's']])
    if (s >= d) return `${(s / d).toFixed(s / d < 10 ? 1 : 0)} ${u}`
  return `${s.toFixed(2)} s`
}
const sci = (v) => {
  if (v < 10) return v.toPrecision(2)
  if (v < 1e4) return Math.round(v).toLocaleString()
  const e = Math.floor(Math.log10(v))
  return `${(v / 10 ** e).toFixed(1)}×10${String(e).split('').map((c) => '⁰¹²³⁴⁵⁶⁷⁸⁹'[c]).join('')}`
}
const PRESETS = [
  { label: 'laptop', t: 8, r: 0 },
  { label: '1 COSMA8 node', t: 16, r: 3 },
  { label: '8 nodes', t: 16, r: 6 },
]
</script>

<template>
  <div class="pc">
    <div class="controls">
      <label>galaxies <b>{{ sci(nGal) }}</b><input v-model.number="logNgal" type="range" min="2" max="8" step="0.1" /></label>
      <label>star particle mass <b>10<sup>{{ logMpart.toFixed(1) }}</sup> M☉</b><input v-model.number="logMpart" type="range" min="4" max="8" step="0.1" /></label>
      <div class="sub">≈ <b>{{ sci(nMean) }}</b> star particles per galaxy (mean, GSMF-weighted) </div>
      <label>threads per rank <b>{{ threads }}</b><input v-model.number="threads" type="range" min="1" max="64" step="1" /></label>
      <label>MPI ranks <b>{{ ranks }}</b><input v-model.number="logRanks" type="range" min="0" max="10" step="1" /></label>
      <div class="presets">
        <button v-for="p in PRESETS" :key="p.label" @click="threads = p.t; logRanks = p.r">{{ p.label }}</button>
      </div>
    </div>

    <div class="out">
      <div class="term">
        <div class="muted"># wall-clock</div>
        <div class="big">{{ human(wall) }}</div>
        <div class="muted mt-3"># CPU-hours</div>
        <div class="big cpu">{{ sci(cpuHours) }}</div>
        <div class="muted small mt-3">{{ sci(nGal * nMean) }} star particles in total · {{ ranks * threads }} cores</div>
      </div>
      <div class="term gets">
        <div class="muted"># and you get</div>
        <table>
          <tbody>
            <tr><td>spectra</td><td><b>{{ sci(nGal * 22) }}</b></td><td>11 emissions × rest + obs · 9,244 λ</td></tr>
            <tr><td>photometry</td><td><b>{{ sci(nGal * 176) }}</b></td><td>11 emissions × 8 NIRCam × L + F</td></tr>
            <tr><td>lines</td><td><b>{{ sci(nGal * 5588) }}</b></td><td>254 lines × 11 emissions × L + F</td></tr>
            <tr><td>images</td><td><b>{{ sci(nGal * 176) }}</b></td><td>11 emissions × 8 NIRCam × rest + obs</td></tr>
            <tr><td>extras</td><td></td><td>SFZH · SFH · LOS τ · per-particle spectra</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pc { display: grid; grid-template-columns: 1fr 1.25fr; gap: 32px; align-items: center; font-size: 0.85rem; }
label { display: block; margin: 10px 0 0; }
label b { color: var(--warn); float: right; }
input[type='range'] { width: 100%; accent-color: var(--accent); }
.sub { font-size: 0.68rem; color: var(--muted); margin: 2px 0 6px; }
.sub b { color: var(--theory); }
.presets { display: flex; gap: 8px; margin-top: 12px; }
.presets button { font-size: 0.65rem; padding: 1px 10px; border: 1px solid var(--line); border-radius: 999px; color: var(--muted); background: transparent; }
.presets button:hover { border-color: var(--accent); color: var(--accent); }
.out { text-align: center; }
.big { font-size: 2.2rem; font-weight: 700; color: var(--accent); line-height: 1.15; font-variant-numeric: tabular-nums; }
.big.cpu { color: var(--warn); }
.small { font-size: 0.65rem; }
.gets { margin-top: 12px; text-align: left; font-size: 0.68rem; }
.gets table { width: 100%; border-collapse: collapse; margin-top: 4px; }
.gets td { padding: 2px 4px; border-bottom: 1px solid var(--grid); }
.gets td:first-child { color: var(--accent); white-space: nowrap; padding-right: 10px; }
.gets td:nth-child(2) { text-align: right; padding-right: 10px; }
.gets td b { color: var(--warn); }
</style>
