import pytest
import os
from dotenv import load_dotenv

@pytest.fixture(autouse=True)
def env_setup():
    """Setup test environment variables."""
    os.environ["NOTION_API_KEY"] = "test-api-key"
    os.environ["NOTION_PAGE_ID"] = "test-page-id" 