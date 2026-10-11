import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_homepage_serves_html():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        assert "SevaGuide" in response.text
        assert "root" in response.text


@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"


@pytest.mark.asyncio
async def test_list_services():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/services")
        assert response.status_code == 200
        services = response.json()
        assert isinstance(services, list)
        assert len(services) >= 3

        slugs = [s["slug"] for s in services]
        assert "income-certificate" in slugs
        assert "caste-certificate" in slugs
        assert "residence-certificate" in slugs


@pytest.mark.asyncio
async def test_service_filtering_and_search():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Filter by category
        res_cat = await ac.get("/api/v1/services?category=Social")
        assert res_cat.status_code == 200
        items_cat = res_cat.json()
        assert len(items_cat) >= 1
        assert any("caste" in i["slug"] for i in items_cat)

        # Search by keyword
        res_search = await ac.get("/api/v1/services?search=residence")
        assert res_search.status_code == 200
        items_search = res_search.json()
        assert len(items_search) >= 1
        assert any("residence" in i["slug"] for i in items_search)


@pytest.mark.asyncio
async def test_get_single_service():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/services/income-certificate")
        assert response.status_code == 200
        svc = response.json()
        assert svc["slug"] == "income-certificate"
        assert "Income Certificate" in svc["title"]
        assert svc["fee"]["amount"] > 0


@pytest.mark.asyncio
async def test_get_service_checklist():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/services/caste-certificate/checklist")
        assert response.status_code == 200
        chk = response.json()
        assert chk["service_slug"] == "caste-certificate"
        assert len(chk["documents_required"]) > 0
        assert len(chk["application_steps"]) > 0
        assert len(chk["eligibility_checklist"]) > 0


@pytest.mark.asyncio
async def test_get_checklist_direct():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/checklists/residence-certificate")
        assert response.status_code == 200
        chk = response.json()
        assert chk["service_slug"] == "residence-certificate"


@pytest.mark.asyncio
async def test_get_nonexistent_service():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/services/nonexistent-service-123")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_service_documents():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/services/income-certificate/documents")
        assert response.status_code == 200
        docs = response.json()
        assert isinstance(docs, list)
        assert len(docs) > 0
        assert "document_name" in docs[0]


@pytest.mark.asyncio
async def test_ai_popular_terms():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/ai/popular-terms")
        assert response.status_code == 200
        terms = response.json()
        assert len(terms) >= 5
        keys = [t["key"] for t in terms]
        assert "domicile" in keys
        assert "creamy layer" in keys


@pytest.mark.asyncio
async def test_ai_explain_term():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {"term": "Creamy Layer", "context": "OBC Certificate"}
        response = await ac.post("/api/v1/ai/explain-term", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "Creamy Layer" in data["term"]
        assert len(data["simplified_explanation"]) > 10
        assert len(data["real_world_example"]) > 10
        assert len(data["actionable_tip"]) > 10


@pytest.mark.asyncio
async def test_ai_check_eligibility():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "service_slug": "income-certificate",
            "user_query": "I am a college student and my parents earn 4 lakh rupees per year. Am I eligible for fee waiver?",
            "applicant_profile": {"annual_income": 400000}
        }
        response = await ac.post("/api/v1/ai/check-eligibility", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["service_slug"] == "income-certificate"
        assert len(data["assessment"]) > 0
        assert len(data["reasoning"]) > 0
        assert len(data["required_documents_highlight"]) > 0


@pytest.mark.asyncio
async def test_ai_check_eligibility_nonexistent_service():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "service_slug": "fake-certificate-999",
            "user_query": "Am I eligible?"
        }
        response = await ac.post("/api/v1/ai/check-eligibility", json=payload)
        assert response.status_code == 404
