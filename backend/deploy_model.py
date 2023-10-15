from google.cloud import aiplatform

def deploy_model():
    aiplatform.init(project='anime-recommender-joppe', location='eu-west1')
    
    model = aiplatform.Model.upload(
        display_name='AnimeRecommender',
        serving_container_image_uri='eu-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-6:latest',
        # Add more parameters if needed
    )
    
    model.deploy(
        deployed_model_display_name='AnimeRecommenderDeployed',
        machine_type='n1-standard-4',
        # Add more parameters if needed
    )

if __name__ == '__main__':
    deploy_model()
