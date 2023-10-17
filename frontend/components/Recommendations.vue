<template>
	<div class="recommendation-container">
		<h2>Recommended Anime</h2>
		<div class="anime-list">
			<div
				v-for="anime in recommendedAnime"
				:key="anime.engName || anime.jpName"
				class="anime-card"
			>
				<h3 class="anime-title">
					<a :href="anime.url">{{
						anime?.name ? anime.name : "Name not available"
					}}</a>
				</h3>
				<p><strong>Score:</strong> {{ anime.score }}</p>

				<div v-if="anime.genres" class="tags">
					<span class="tag" v-for="genre in anime.genres" :key="genre">{{
						genre
					}}</span>
				</div>

				<div v-if="anime.themes" class="tags">
					<span class="tag" v-for="theme in anime.themes" :key="theme">{{
						theme
					}}</span>
				</div>

				<p v-if="anime.aired"><strong>Aired:</strong> {{ anime.aired }}</p>
				<p v-if="anime.producer">
					<strong>Producer:</strong> {{ anime.producer }}
				</p>
				<p v-if="anime.studios">
					<strong>Studios:</strong> {{ anime.studios.join(", ") }}
				</p>
				<!-- all rank -->
				<p v-if="anime.allRank"><strong>Rank </strong> {{ anime.allRank }}</p>
			</div>
		</div>
	</div>
</template>

<!-- consentual -->
<script setup>
	const props = defineProps(["recommendedAnime"]);
</script>

<style scoped lang="scss">
	.recommendation-container {
		font-family: "Arial", sans-serif;

		h2 {
			text-align: center;
			color: #2c3e50;
			margin-bottom: 20px;
		}

		.anime-list {
			display: flex;
			flex-wrap: wrap;
			justify-content: space-around;
		}

		.anime-card {
			background: #f7f7f7;
			border: 1px solid #e7e7e7;
			border-radius: 8px;
			padding: 15px;
			margin: 15px;
			width: 100%; // Default to single column for mobile
			box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
			transition: box-shadow 0.3s ease;
			box-sizing: border-box;

			&:hover {
				box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
			}

			.anime-title {
				margin-top: 0;
				margin-bottom: 10px;

				a {
					text-decoration: none;
					color: #3498db;
					transition: color 0.3s ease;

					&:hover {
						color: #2980b9;
					}
				}
			}

			p {
				margin-bottom: 10px;
				color: #34495e;

				strong {
					color: #2c3e50;
				}
			}

			.tags {
				display: flex;
				flex-wrap: wrap;
				margin: 8px 0;

				.tag {
					background-color: #e1e1e1;
					color: #333;
					padding: 2px 8px;
					border-radius: 14px;
					margin: 2px;
					font-size: 0.9rem;
				}
			}
		}

		// Tablet layout
		@media (min-width: 768px) {
			.anime-card {
				margin: 20px;
			}
		}

		// Laptop layout with 2 columns
		@media (min-width: 1024px) {
			.anime-card {
				width: calc(50% - 20px); // Shorten distance between two columns
				margin: 10px;
			}
		}

		// Desktop layout with 3 columns
		@media (min-width: 1200px) {
			.anime-card {
				width: calc(33% - 20px);
				margin: 15px;
			}
		}
	}
</style>
