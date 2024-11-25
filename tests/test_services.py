import pytest
from app.services.github_service import fetch_repo_contents
from app.services.ai_service import generate_review
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_fetch_repo_contents():
    with patch("aiohttp.ClientSession.get", new_callable=AsyncMock) as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = [{"name": "file1.py"}, {"name": "file2.py"}]
        mock_get.return_value.__aenter__.return_value = mock_response

        repo_contents = await fetch_repo_contents("https://github.com/test/test-repo")
        assert len(repo_contents) == 2
        assert repo_contents[0]["name"] == "file1.py"

@pytest.mark.asyncio
async def test_generate_review():
    mock_repo_contents = [{"name": "file1.py"}, {"name": "file2.py"}]
    with patch("openai.ChatCompletion.create", new_callable=AsyncMock) as mock_openai:
        mock_openai.return_value.choices = [{"message": {"content": "Test review content"}}]

        review = await generate_review("Test assignment", mock_repo_contents, "Junior")
        assert "Test review content" in review
