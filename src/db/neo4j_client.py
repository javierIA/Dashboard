import logging
from contextlib import asynccontextmanager
from db.model import seriaizer_organitation, serializer_location, serializer_researcher, serializer_knowledgediscipline
from neo4j import (
    basic_auth,
    AsyncGraphDatabase,
)


class Neo4jClient:
    def __init__(self):
        self.url = "bolt://ec2-54-227-173-99.compute-1.amazonaws.com:7687"
        self.username = "neo4j"
        self.password = "password"
        self.database = "neo4j"
        self.neo4j_version = "5.3.0"
        self.driver = AsyncGraphDatabase.driver(
            self.url, auth=basic_auth(self.username, self.password))
        self.logger = logging.getLogger(__name__)

    @asynccontextmanager
    async def get_db(self):
        if self.neo4j_version >= "4":
            async with self.driver.session(database=self.database) as session_:
                yield session_
        else:
            async with self.driver.session() as session_:
                yield session_

    async def get_dashboard(self):
        async def work(tx):
            result = await tx.run(
                """MATCH (o)-[:HAS]->(r:Researcher)
            WHERE (o:Organization OR o:AcademicInstitution OR o:GovermentInstitution) AND r IS NOT NULL
            OPTIONAL MATCH (r)-[:INTERESTED_IN]->(k)
            OPTIONAL MATCH (o)-[:LOCATED_IN]->(c:City)
            RETURN DISTINCT
                o.name as Organization,
                o.location_point.x as X,
                o.location_point.y as Y,
                labels(o) as OrganizationType,
                r.name as Researcher,
                r.second_surname as Surname,
                k.description as Knowledge,
                labels(k) as KnowledgeType,
                c.name as City""")
            return [record_ async for record_ in result]

        async with self.get_db() as db:
            results = await db.execute_read(work)
            nodes = []
            rels = []
            i = 0
            for record in results:
                nodes.append(record)
                target = i
                i += 1
                rels.append({"source": 0, "target": target})

            return nodes

    async def close(self):
        await self.driver.close()
