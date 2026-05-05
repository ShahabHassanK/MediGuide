import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))


class Settings:
    def __init__(self):
        self.groq_api_key = self._require('GROQ_API_KEY')
        self.qdrant_url = self._require('QDRANT_URL')
        self.qdrant_api_key = self._require('QDRANT_API_KEY')
        self.qdrant_collection_name = os.getenv('QDRANT_COLLECTION_NAME', 'mediaguide_knowledge')
        self.neo4j_uri = self._require('NEO4J_URI')
        self.neo4j_username = self._require('NEO4J_USERNAME')
        self.neo4j_password = self._require('NEO4J_PASSWORD')
        self.neo4j_database = os.getenv('NEO4J_DATABASE', 'neo4j')
        self.cors_origins = os.getenv(
            'CORS_ORIGINS',
            'http://localhost:5173,http://127.0.0.1:5173'
        ).split(',')

    def _require(self, key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Missing required environment variable: {key}")
        return value


settings = Settings()
