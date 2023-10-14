<template>
  <div>
    <h2>Recommended Anime</h2>
    <div v-for="anime in recommendedAnime" :key="anime.name">
      <div class="recommendation">
        <h3>
          <a :href="anime.url">{{ anime.name }}</a>
        </h3>
        <p>Score: {{ anime.score }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps(['recommendedAnime']);
</script>
