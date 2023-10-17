<template>
  <div class="recommendation-container">
    <h2>Recommended Anime</h2>
    <div class="anime-list">
      <div v-for="anime in recommendedAnime" :key="anime.engName || anime.jpName" class="anime-item">
        <h3>
          <a :href="anime.url">{{ anime?.name ? anime.name : 'Name not available' }}</a>
        </h3>
        <p>Score: {{ anime.score }}</p>
        <p v-if="anime.genres">Genres: {{ anime.genres }}</p>
        <p v-if="anime.themes">Themes: {{ anime.themes }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps(['recommendedAnime']);
</script>

<style scoped lang="scss">
.recommendation-container {
  font-family: 'Arial', sans-serif;
  max-width: 700px;
  margin: 50px auto;
  padding: 20px;
  box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
  border-radius: 8px;

  h2 {
    color: #2c3e50;
    margin-bottom: 20px;
    text-align: center;
    border-bottom: 2px solid #e74c3c;
    padding-bottom: 15px;
  }

  .anime-list {
    margin-top: 20px;

    .anime-item {
      margin-bottom: 20px;
      padding: 15px;
      border-radius: 6px;
      background-color: #f9f9f9;
      transition: background-color 0.3s ease;

      &:hover {
        background-color: #e9e9e9;
      }

      h3 {
        margin: 0;
        margin-bottom: 10px;
        a {
          color: #2980b9;
          text-decoration: none;
          transition: color 0.3s ease;

          &:hover {
            color: #e74c3c;
          }
        }
      }

      p {
        margin: 0;
        color: #7f8c8d;
      }
    }
  }
}
</style>