<script setup>
// Small merger-tree schematic: haloes (circles sized by mass) at each
// snapshot, linked to their descendants, merging into one main branch.
const SNAPS = [20, 60, 100, 140, 180]
// [snapshot index, x, radius]
const NODES = [
  [0, 30, 5], [0, 70, 4], [0, 110, 6], [0, 150, 3],
  [1, 50, 8], [1, 110, 7], [1, 150, 4],
  [2, 70, 11], [2, 140, 6],
  [3, 90, 14],
  [4, 90, 17],
]
const LINKS = [[0, 4], [1, 4], [2, 5], [3, 6], [4, 7], [5, 7], [6, 8], [7, 9], [8, 9], [9, 10]]
const y = (i) => SNAPS[NODES[i][0]]
const main = new Set([2, 5, 7, 9, 10])
</script>

<template>
  <svg viewBox="0 0 180 205" class="tree">
    <text v-for="(s, i) in SNAPS" :key="s" x="2" :y="s + 3" class="t">t{{ i }}</text>
    <line
      v-for="([a, b], k) in LINKS"
      :key="k"
      :x1="NODES[a][1]" :y1="y(a)" :x2="NODES[b][1]" :y2="y(b)"
      :class="['link', { main: main.has(a) && main.has(b) }]"
    />
    <circle v-for="(n, i) in NODES" :key="i" :cx="n[1]" :cy="y(i)" :r="n[2]" :class="['halo', { main: main.has(i) }]" />
  </svg>
</template>

<style scoped>
.tree { height: 100%; font-family: var(--mono); }
.t { fill: var(--muted); font-size: 9px; }
.link { stroke: #666; stroke-width: 1.5; }
.link.main { stroke: var(--accent); stroke-width: 2.5; }
.halo { fill: #111; stroke: var(--theory); stroke-width: 1.5; }
.halo.main { fill: color-mix(in srgb, var(--accent) 25%, #000); stroke: var(--accent); }
</style>
