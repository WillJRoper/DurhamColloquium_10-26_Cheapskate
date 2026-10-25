<script setup>
// Regions sampled from a big box, each blown up into its own zoom
// (after the TESSERA title slide). Drawn in a 600x720 frame; the circular
// insets are HTML so the images clip cleanly.
const ZOOMS = [
  { rx: 95, ry: 130, rr: 13, cx: 400, cy: 130, r: 95, img: 'tessera/title_zoom_a.webp' },
  { rx: 120, ry: 360, rr: 15, cx: 440, cy: 360, r: 110, img: 'tessera/title_zoom_b.webp' },
  { rx: 85, ry: 590, rr: 12, cx: 395, cy: 590, r: 90, img: 'tessera/title_zoom_c.webp' },
]
const pct = (v, of) => `${(v / of) * 100}%`
const base = import.meta.env.BASE_URL
</script>

<template>
  <div class="callouts">
    <img :src="`${base}tessera/title_strip.webp`" class="strip" alt="large-volume parent simulation" />
    <svg viewBox="0 0 600 720" preserveAspectRatio="none" class="overlay">
      <g v-for="z in ZOOMS" :key="z.img">
        <path :d="`M ${z.rx} ${z.ry} L ${z.cx} ${z.cy - z.r} L ${z.cx} ${z.cy + z.r} Z`" class="cone" />
        <circle :cx="z.rx" :cy="z.ry" :r="z.rr" class="region" />
      </g>
    </svg>
    <div
      v-for="z in ZOOMS"
      :key="`i${z.img}`"
      class="slot"
      :style="{ left: pct(z.cx - z.r, 600), top: pct(z.cy - z.r, 720), width: pct(2 * z.r, 600) }"
    >
      <img :src="base + z.img" alt="zoom region" />
    </div>
  </div>
</template>

<style scoped>
.callouts { position: relative; height: 100%; aspect-ratio: 600 / 720; }
.strip {
  position: absolute; left: 0; top: 0; height: 100%; width: 35%; object-fit: cover;
  -webkit-mask-image: linear-gradient(to right, black 40%, transparent 95%);
  mask-image: linear-gradient(to right, black 40%, transparent 95%);
}
.overlay { position: absolute; inset: 0; width: 100%; height: 100%; }
.region { fill: none; stroke: var(--warn); stroke-width: 3; }
.cone { fill: rgba(255, 255, 255, 0.06); stroke: #888; stroke-width: 1.2; }
.slot { position: absolute; aspect-ratio: 1; border-radius: 9999px; overflow: hidden; border: 2.5px solid var(--warn); background: #000; }
.slot img { width: 100%; height: 100%; object-fit: cover; }
</style>
