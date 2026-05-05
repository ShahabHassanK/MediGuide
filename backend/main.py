import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from api.routes import chat, voice, documents

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Verify Qdrant connection
    try:
        from db.qdrant_client import get_qdrant_client
        client = get_qdrant_client()
        client.get_collections()
        logger.info("Qdrant connected successfully")
    except Exception as e:
        logger.error(f"Qdrant connection failed: {e}")

    # Verify Neo4j connection
    try:
        from db.neo4j_client import run_query
        run_query("RETURN 1 AS n")
        logger.info("Neo4j connected successfully")
    except Exception as e:
        logger.error(f"Neo4j connection failed: {e}")

    # Pre-load embedding model
    try:
        from ingestion.embedder import embed_single
        embed_single("warmup")
        logger.info("Embedding model loaded successfully")
    except Exception as e:
        logger.error(f"Embedding model load failed: {e}")

    yield

    # Shutdown: close Neo4j driver
    try:
        from db.neo4j_client import get_neo4j_driver
        get_neo4j_driver().close()
        logger.info("Neo4j driver closed")
    except Exception:
        pass


app = FastAPI(title="MediGuide API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api")
app.include_router(voice.router, prefix="/api/voice")
app.include_router(documents.router, prefix="/api/documents")


@app.get("/")
async def health():
    return {"status": "ok"}
