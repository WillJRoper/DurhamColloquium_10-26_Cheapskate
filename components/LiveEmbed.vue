<script setup>
// Live website in a terminal-style window, with a screenshot when offline.
// The slide canvas is only ~980px wide, so a plain iframe gets the site's
// cramped narrow layout. Instead the iframe is laid out at `width` px (a
// desktop viewport) and scaled down to fit the window.
import { ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  src: { type: String, required: true },
  fallback: { type: String, default: '' },
  width: { type: Number, default: 1440 },
})
const online = ref(true)
const box = ref(null)
const scale = ref(1)
const height = ref(800)
let ro
onMounted(() => {
  online.value = navigator.onLine
  ro = new ResizeObserver(() => {
    const el = box.value
    if (!el) return
    scale.value = el.offsetWidth / props.width
    height.value = el.offsetHeight / scale.value
  })
  ro.observe(box.value)
})
onBeforeUnmount(() => ro?.disconnect())
</script>

<template>
  <div class="embed term">
    <div class="term-bar"><span /><span /><span /><a :href="src" target="_blank" class="url">{{ src }} ↗</a></div>
    <div ref="box" class="view">
      <iframe
        v-if="online"
        :src="src"
        loading="lazy"
        :style="{ width: `${width}px`, height: `${height}px`, transform: `scale(${scale})` }"
      />
      <img v-else-if="fallback" :src="fallback" alt="offline screenshot" />
    </div>
  </div>
</template>

<style scoped>
.embed { height: 100%; display: flex; flex-direction: column; padding: 0.5rem; }
.term-bar { align-items: center; margin: 0 0 0.4rem; }
.url { margin-left: 10px; font-size: 0.65rem; color: var(--muted); border: none; }
.view { flex: 1; position: relative; overflow: hidden; border-radius: 4px; background: #fff; }
iframe { position: absolute; top: 0; left: 0; border: 0; transform-origin: 0 0; }
img { width: 100%; height: 100%; object-fit: contain; object-position: top; }
</style>
