<script setup>
// Initial conditions -> supercomputer (+ physics) -> simulation.
// step: 0 ICs, 1 ICs flow in, 2 physics chips join, 3 simulation comes out.
defineProps({ step: { type: Number, default: 3 } })
const base = import.meta.env.BASE_URL

const physics = [
  'Gravity', 'Hydrodynamics', 'Cosmology', 'Cooling',
  'Star formation', 'Stellar feedback', 'Black holes', 'AGN feedback',
  'Chemical enrichment', 'Dust',
]
</script>

<template>
  <div class="machine">
    <div class="col">
      <img :src="`${base}img/ics.png`" class="panel" alt="initial conditions density field" />
      <div class="cap">initial conditions</div>
    </div>

    <div :class="['pipe', { on: step >= 1 }]"><span /></div>

    <div class="col mid">
      <div class="chips">
        <span v-for="(p, i) in physics" :key="p" :class="['chip', { on: step >= 2 }]" :style="{ transitionDelay: `${i * 70}ms` }">{{ p }}</span>
      </div>
      <div :class="['computer', { busy: step >= 2 }]">
        <img :src="`${base}img/cosma.png`" alt="COSMA supercomputer" />
        <img :src="`${base}img/swift_logo.png`" class="logo" alt="SWIFT" />
      </div>
      <div class="cap">supercomputer + code + physics</div>
    </div>

    <div :class="['pipe', { on: step >= 3 }]"><span /></div>

    <div class="col">
      <div class="panel out">
        <video v-if="step >= 3" :src="`${base}video/eagle_galaxy_evolution.mp4`" autoplay loop muted playsinline />
      </div>
      <div class="cap">a simulated universe</div>
    </div>
  </div>
</template>

<style scoped>
.machine { display: grid; grid-template-columns: 1fr 70px 1.5fr 70px 1fr; align-items: center; gap: 4px; }
.col { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.panel { width: 100%; aspect-ratio: 1; object-fit: cover; border: 1px solid var(--line); border-radius: 6px; background: #050505; overflow: hidden; }
.out video { width: 100%; height: 100%; object-fit: cover; }
.cap { font-size: 0.75rem; color: var(--muted); }
.pipe { height: 6px; background: #1a1a1a; border-radius: 3px; overflow: hidden; position: relative; }
.pipe span { position: absolute; inset: 0; opacity: 0; background: repeating-linear-gradient(90deg, var(--accent) 0 10px, transparent 10px 20px); background-size: 20px 100%; }
.pipe.on span { opacity: 1; animation: pump 0.6s linear infinite; }
@keyframes pump { to { background-position: 20px 0; } }
.chips { display: flex; flex-wrap: wrap; gap: 5px; justify-content: center; min-height: 64px; }
.chip { font-size: 0.78rem; padding: 3px 9px; border: 1px solid var(--theory); color: var(--theory); border-radius: 4px; opacity: 0; transform: translateY(-14px); transition: all 0.4s; }
.chip.on { opacity: 1; transform: none; }
.computer { position: relative; width: 100%; border: 1px solid var(--line); border-radius: 6px; overflow: hidden; }
.computer img:first-child { width: 100%; display: block; filter: brightness(0.55); transition: filter 0.6s; }
.computer.busy img:first-child { filter: brightness(1); animation: hum 1.6s ease-in-out infinite; }
@keyframes hum { 50% { filter: brightness(1.25) saturate(1.3); } }
.logo { position: absolute; left: 50%; top: 50%; width: 55%; transform: translate(-50%, -50%); filter: invert(1) drop-shadow(0 0 6px #000); }
</style>
