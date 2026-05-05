from neo4j import GraphDatabase, Driver
from config import settings

_driver: Driver | None = None


def get_neo4j_driver() -> Driver:
    global _driver
    if _driver is None:
        # neo4j+ssc:// uses encryption but skips cert verification (needed on Windows with AuraDB)
        uri = settings.neo4j_uri.replace("neo4j+s://", "neo4j+ssc://").replace("bolt+s://", "bolt+ssc://")
        _driver = GraphDatabase.driver(
            uri,
            auth=(settings.neo4j_username, settings.neo4j_password),
        )
    return _driver


def run_query(cypher: str, params: dict = {}) -> list[dict]:
    driver = get_neo4j_driver()
    with driver.session(database=settings.neo4j_database) as session:
        result = session.run(cypher, params)
        return [record.data() for record in result]
