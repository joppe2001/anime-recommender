<template>
  <div>
    <AnimeInput @recommendations="updateRecommendations" />
    <Recommendations :recommendedAnime="recommendations" />
  </div>
</template>

<script setup>

const recommendations = ref([]);

function updateRecommendations(newRecommendations) {
  recommendations.value = newRecommendations;
}
</script>
