<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <div class="flex justify-center ">
    <img src="./assets/cargps_logo.webp" class="logo" alt="Car logo" />
  </div>
  <HelloWorld msg="Car Tracker" />
</template>

<style scoped>
.logo {
  height: 12em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #c7c7c7aa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
