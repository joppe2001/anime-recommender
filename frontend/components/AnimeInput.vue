<template>
  <div>
    <h2>Enter Anime Names</h2>
    <form @submit.prevent="getRecommendations">
      <label for="animeInput">Enter anime names (comma separated):</label>
      <input type="text" id="animeInput" v-model="animeInput" />
      <button type="submit">Get Recommendations</button>
    </form>
  </div>
</template>

<script setup>

const emit = defineEmits()

const animeInput = ref("");

async function getRecommendations() {
  const inputArray = animeInput.value.split(",");
  // Make API request to the Flask backend
  const response = await fetch("https://127.0.0.1:3000/recommend", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_history: inputArray }),
  });
  
  const data = await response.json();
  // Emitting event to parent component
  emit("recommendations", data);
}
</script>

<style scoped>
/* Your CSS styling here */
</style>
