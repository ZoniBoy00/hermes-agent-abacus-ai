"""Test configuration and shared fixtures for abacus_ai plugin tests."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Generator
from unittest.mock import MagicMock, patch

import pytest

# Add the plugin dir so imports work
_PLUGIN_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PLUGIN_DIR))


@pytest.fixture(autouse=True)
def reset_env() -> Generator[None, None, None]:
    """Ensure clean environment for each test."""
    old = dict(os.environ)
    # Remove any Abacus AI env vars that might be set
    for key in list(os.environ.keys()):
        if key.startswith("ABACUS_AI_") or key.startswith("HONCHO_"):
            del os.environ[key]
    yield
    os.environ.clear()
    os.environ.update(old)


@pytest.fixture
def mock_requests_post() -> Generator[MagicMock, None, None]:
    """Mock ``requests.post`` to return a fake Abacus AI response."""
    fake_image_data = (
        "data:image/png;base64,"
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk"
        "YPhfDwABQAEALL0BzQAAAABJRU5ErkJggg=="
    )

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "",
                    "images": [
                        {
                            "type": "image_url",
                            "image_url": {"url": fake_image_data},
                        }
                    ],
                }
            }
        ]
    }

    with patch("requests.post", return_value=mock_response) as mock:
        yield mock


@pytest.fixture
def mock_credentials() -> Generator[None, None, None]:
    """Set mock Abacus AI credentials."""
    os.environ["ABACUS_AI_API_KEY"] = "test-key-123"
    os.environ["ABACUS_AI_BASE_URL"] = "https://test.api.example.com/v1"
    yield
