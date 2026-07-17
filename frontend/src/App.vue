<template>
  <div class="min-h-screen relative">
    <div class="star-bg">
      <div
        v-for="i in 100"
        :key="i"
        class="star"
        :style="getStarStyle(i)"
      ></div>
    </div>
    <router-view />
  </div>
</template>

<script setup>
const getStarStyle = (index) => ({
  left: `${Math.random() * 100}%`,
  top: `${Math.random() * 100}%`,
  width: `${Math.random() * 3 + 1}px`,
  height: `${Math.random() * 3 + 1}px`,
  '--duration': `${Math.random() * 2 + 2}s`,
  '--delay': `${Math.random() * 3}s`,
})
</script>
