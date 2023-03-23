import asyncio
import logging
from contextlib import asynccontextmanager
from neo4j import (
    basic_auth,
    AsyncGraphDatabase,
)
import os


class Neo4jClient:
    def __init__(self):

        self.url = os.getenv("URL")
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.database = os.getenv("DATABASE", "neo4j")
        self.neo4j_version = os.getenv("NEO4J_VERSION", "5.3")
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
            WHERE (o:Organization OR o:AcademicInstitution OR o:GovermentInstitution OR o:Enterprise) AND r IS NOT NULL
            OPTIONAL MATCH (r)-[:INTERESTED_IN]->(k)
            OPTIONAL MATCH (o)-[:LOCATED_IN]->(c:City)
            RETURN DISTINCT
                o.name as Organization,
                o.location_point.x as X,
                o.location_point.y as Y,
                labels(o) as OrganizationType,
                r.name as Researcher,
                r.second_surname as Surname,
                r.identifier as Id,
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

    async def get_investigation_data(self, uuid_list):

        async def work(tx):
            uuids = ','.join(f'"{uuid}"' for uuid in uuid_list)
            query = f"""MATCH (r:Researcher)-[:PARTICIPATED_IN]->(s:ScientificPaper)
    WHERE r.identifier IN [{uuids}]
    RETURN COUNT(s)"""
            result = await tx.run(query)
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
                pass
            return nodes

    async def close(self):
        await self.driver.close()
