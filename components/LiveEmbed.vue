<script setup>
// Live website in a terminal-style window, with a screenshot when offline.
import { ref, onMounted } from 'vue'

const props = defineProps({
  src: { type: String, required: true },
  fallback: { type: String, default: '' },
})
const online = ref(true)
onMounted(() => { online.value = navigator.onLine })
</script>

<template>
  <div class="embed term">
    <div class="term-bar"><span /><span /><span /><a :href="src" target="_blank" class="url">{{ src }}</a></div>
    <iframe v-if="online" :src="src" loading="lazy" />
    <img v-else-if="fallback" :src="fallback" alt="offline screenshot" />
  </div>
</template>

<style scoped>
.embed { height: 100%; display: flex; flex-direction: column; padding: 0.5rem; }
.term-bar { align-items: center; margin: 0 0 0.4rem; }
.url { margin-left: 10px; font-size: 0.65rem; color: var(--muted); border: none; }
iframe, img { flex: 1; width: 100%; border: 0; border-radius: 4px; background: #fff; object-fit: contain; object-position: top; }
</style>
