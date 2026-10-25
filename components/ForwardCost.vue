<script setup>
// Forward modelling as a stack of choices: each click adds one modelling
// choice (with a handful of reasonable options) and the running count of
// models you'd need to cover them all multiplies up. The last click puts the
// simulation on the other side: galaxies x particles x wavelengths.
import { computed } from 'vue'

const props = defineProps({ step: { type: Number, default: 0 } })

const CHOICES = [
  { name: 'SPS library', opts: ['BC03', 'BPASS', 'FSPS', 'Maraston'] },
  { name: 'IMF', opts: ['Chabrier', 'Kroupa', 'Salpeter', 'top-heavy'] },
  { name: 'nebular', opts: ['log U', 'n_H', 'geometry'], range: true },
  { name: 'dust curve', opts: ['Calzetti', 'SMC', 'power law'] },
  { name: 'dust geometry', opts: ['screen', 'birth cloud + ISM', 'line of sight'] },
  { name: 'escape fraction', opts: ['0', '0.1', '0.3'], range: true },
  { name: 'instrument', opts: ['JWST', 'HST', 'Euclid', 'Rubin'] },
]
const shown = computed(() => Math.min(props.step, CHOICES.length))
const models = computed(() => CHOICES.slice(0, shown.value).reduce((p, c) => p * c.opts.length, 1))
const fmt = (n) => n.toLocaleString()
const final = computed(() => props.step > CHOICES.length)
</script>

<template>
  <div class="fc">
    <div class="cards">
      <div v-for="(c, i) in CHOICES" :key="c.name" :class="['card', { on: i < shown }]">
        <div class="name">{{ c.name }}</div>
        <div class="opts">
          <span v-for="o in c.opts" :key="o">{{ o }}</span><span v-if="c.range" class="rng">…continuous</span>
        </div>
        <div class="n">× {{ c.opts.length }}</div>
      </div>
    </div>

    <div class="tally">
      <div class="muted">model variations to cover the choices</div>
      <div class="big">≳ {{ fmt(models) }}</div>
      <div class="note">indicative: many of these are continuous ranges, not a handful of options</div>
      <div :class="['sim', { on: final }]">
        <div class="muted">...then, for every one of them</div>
        <div class="mult">× N<sub>gal</sub> × N<sub>part</sub> × N<sub>λ</sub></div>
        <div class="punch">So it has to be <b>flexible</b> <em>and</em> <b>cheap</b>.</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fc { display: grid; grid-template-columns: 1.5fr 1fr; gap: 28px; align-items: center; font-size: 0.8rem; }
.cards { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.card { border: 1px solid var(--line); border-radius: 6px; padding: 6px 10px; background: #0a0a0a; opacity: 0.12; transform: translateY(6px); transition: all 0.35s; position: relative; }
.card.on { opacity: 1; transform: none; border-color: color-mix(in srgb, var(--theory) 60%, var(--line)); }
.name { color: var(--theory); }
.opts { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px; }
.opts span { font-size: 0.65rem; padding: 0 6px; border: 1px solid #333; border-radius: 3px; color: var(--muted); }
.opts span.rng { border-style: dashed; color: var(--warn); }
.n { position: absolute; top: 6px; right: 10px; color: var(--warn); font-weight: 700; }
.tally { text-align: center; }
.big { font-size: 3rem; font-weight: 700; color: var(--warn); line-height: 1.1; margin: 4px 0 4px; font-variant-numeric: tabular-nums; }
.note { font-size: 0.62rem; color: var(--muted); margin-bottom: 16px; }
.sim { opacity: 0; transition: opacity 0.4s; }
.sim.on { opacity: 1; }
.mult { color: var(--ink); margin: 6px 0 18px; font-size: 1.5rem; }
.punch { font-size: 1.05rem; }
.punch b { color: var(--warn); }
</style>
