<template>
  <div class="container">
    <h2>Enter Anime Names</h2>
    <form @submit.prevent="getRecommendations">
      <div class="input-group">
        <label for="animeInput">Enter anime names (comma separated):</label>
        <input type="text" id="animeInput" v-model="animeInput" />
      </div>
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
  const response = await fetch("https://new-recommender.ew.r.appspot.com/recommend", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_history: inputArray }),
  });
  
  const data = await response.json();
  // Emitting event to parent component
  emit("recommendations", data);
}
</script>

<style scoped lang="scss">
.container {
  font-family: 'Arial', sans-serif;
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
  border-radius: 8px;

  h2 {
    color: #2c3e50;
    margin-bottom: 20px;
    text-align: center;
  }

  .input-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 15px;

    label {
      margin-bottom: 10px;
      font-size: 1.1rem;
      color: #34495e;
    }

    input {
      padding: 10px;
      border: 1px solid #bdc3c7;
      border-radius: 4px;
      font-size: 1rem;
      transition: border-color 0.3s ease;

      &:focus {
        border-color: #2980b9;
        outline: none;
      }
    }
  }

  button {
    cursor: pointer;
    background-color: #3498db;
    color: #fff;
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    font-size: 1.1rem;
    transition: background-color 0.3s ease;

    &:hover {
      background-color: #2980b9;
    }

    &:active {
      background-color: #2471a3;
    }

    &:focus {
      outline: none;
    }
  }
}
</style>
