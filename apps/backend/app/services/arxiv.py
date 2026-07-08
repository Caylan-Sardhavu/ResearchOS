import xml.etree.ElementTree as ET
from app.models.paper import Paper

import httpx


class ArxivService:
    BASE_URL = "https://export.arxiv.org/api/query"

    async def search(self, query: str, max_results: int = 5) -> list[Paper]:
        params = {
            "search_query": f"all:{query}",
            "start": "0",
            "max_results": str(max_results),
        }

        async with httpx.AsyncClient(
            timeout=30,
            follow_redirects=True,
            headers={"User-Agent": "ResearchOS/0.1"},
        ) as client:
            response = await client.get(self.BASE_URL, params=params)

        response.raise_for_status()

        return self._parse_response(response.text)

    def _parse_response(self, xml_text: str) -> list[dict]:
        namespace = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom",
        }

        root = ET.fromstring(xml_text)
        papers = []

        for entry in root.findall("atom:entry", namespace):
            title = entry.findtext("atom:title", default="", namespaces=namespace)
            summary = entry.findtext("atom:summary", default="", namespaces=namespace)
            published = entry.findtext("atom:published", default="", namespaces=namespace)
            url = entry.findtext("atom:id", default="", namespaces=namespace)

            authors = [
                author.findtext("atom:name", default="", namespaces=namespace)
                for author in entry.findall("atom:author", namespace)
            ]

            pdf_url = None
            for link in entry.findall("atom:link", namespace):
                if link.attrib.get("title") == "pdf":
                    pdf_url = link.attrib.get("href")

            papers.append(
                Paper(
                    title=title,
                    authors=authors,
                    summary=summary,
                    published=published,
                    url=url,
                    pdf_url=pdf_url,
                    source="arXiv",
                )
            )

        return papers