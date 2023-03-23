import asyncio
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from neo4j import (
    basic_auth,
    AsyncGraphDatabase,
)
import os


class Neo4jClient:
    def __init__(self):
        load_dotenv()

        self.url = os.getenv("URL")
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.database = os.getenv("DATABASE")
        self.neo4j_version = os.getenv("NEO4J_VERSION")
        self.driver = AsyncGraphDatabase.driver(
            self.url, auth=basic_auth(self.username, self.password)
        )
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
                    c.name as City"""
            )
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
            uuids = ",".join(f'"{uuid}"' for uuid in uuid_list)
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

    async def get_researchers(self):
        async def work(tx):
            result = await tx.run(
                """MATCH (r:Researcher)
                    OPTIONAL MATCH (r)-[]->(country:Country)
                    OPTIONAL MATCH (r)-[]->(state:State)
                    OPTIONAL MATCH (r)-[]->(city:City)
                    OPTIONAL MATCH (r)-[]->(area:KnowledgeArea)
                    OPTIONAL MATCH (r)-[]->(field:KnowledgeField)
                    OPTIONAL MATCH (r)-[]->(discipline:KnowledgeDiscipline)
                    OPTIONAL MATCH (r)<-[:HAS]-(institution:Institution)
                    RETURN 
                    r.cvu as cvu,
                    r.name as name,
                    r.first_surname + '' + r.second_surname as surname,
                    r.sni_level as sni_level,
                    r.identifier as identifier,
                    country.name as country,
                    state.name as state,
                    city.name as city,
                    (CASE WHEN city IS NOT NULL THEN city.latitude 
                        ELSE (CASE WHEN state IS NOT NULL THEN state.latitude 
                            ELSE (CASE WHEN country IS NOT NULL THEN country.latitude 
                            ELSE null END) END) END) as lat, 
                    (CASE WHEN city IS NOT NULL THEN city.longitude 
                        ELSE (CASE WHEN state IS NOT NULL THEN state.longitude 
                            ELSE (CASE WHEN country IS NOT NULL THEN country.longitude 
                            ELSE null END) END) END) as lon,
                    COLLECT(DISTINCT(area.description)) as areas,
                    COLLECT(DISTINCT(field.description)) as fields,
                    COLLECT(DISTINCT(discipline.description)) as disciplines,
                    COLLECT(DISTINCT(institution.name)) as institutions
                    ORDER BY r.cvu"""
            )
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

    async def get_papers(self):
        async def work(tx):
            result = await tx.run(
                """MATCH (p)
    WHERE 
    (p:ScientificPaper OR p:Patent OR p:ResearchProject OR p:ResearchGroup)
    AND p.persistent = True
    WITH p
    OPTIONAL MATCH (p)-[]->(area:KnowledgeArea)
    OPTIONAL MATCH (p)-[]->(field:KnowledgeField)
    OPTIONAL MATCH (p)-[]->(discipline:KnowledgeDiscipline)
    OPTIONAL MATCH (p)<-[]-(researcher:Researcher)
    RETURN 
    CASE WHEN p.title IS NOT NULL THEN p.title ELSE p.name END as name,
    HEAD(labels(p)) as type,
    researcher.identifier as researcher_identifier,
    area.identifier as area_identifier,
    field.identifier as field_identifier,
    discipline.identifier as discipline_identifier"""
            )
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

    async def get_institutions(self):
        async def work(tx):
            result = await tx.run(
                """MATCH (i:Institution)
OPTIONAL MATCH (i)-[]->(country:Country)
OPTIONAL MATCH (i)-[]->(state:State)
OPTIONAL MATCH (i)-[]->(city:City)
OPTIONAL MATCH (r:Researcher)<-[:HAS]-(i)
RETURN 
 i.name as name,
 i.type as type,
 country.name as country,
 state.name as state,
 city.name as city,
 i.location_point as location_point,
 COUNT(r) as num_researchers
ORDER BY i.name"""
            )
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

    async def get_custom_query(self, query):
        async def work(tx):
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

            return nodes

    async def close(self):
        await self.driver.close()
