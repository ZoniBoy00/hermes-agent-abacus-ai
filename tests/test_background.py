"""Tests for background image generation."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from abacus_ai.background import (
    image_generate_background_handler,
    image_generate_background_status_handler,
)


class TestBackgroundHandler:
    """Tests for background image generation handler."""

    def test_missing_prompt_returns_error(self) -> None:
        result = json.loads(
            image_generate_background_handler({"prompt": ""})
        )
        assert result.get("success") is False
        assert "Prompt is required" in result.get("error", "")

    def test_valid_request_returns_job_id(self) -> None:
        result = json.loads(
            image_generate_background_handler(
                {"prompt": "A beautiful sunset"}
            )
        )
        assert result.get("success") is True
        assert "job_id" in result
        assert len(result["job_id"]) == 12
        assert result.get("status") == "queued"

    def test_returns_job_id_for_batch(self) -> None:
        result = json.loads(
            image_generate_background_handler(
                {
                    "jobs": [
                        {"prompt": "Sunset"},
                        {"prompt": "Mountain"},
                    ]
                }
            )
        )
        assert result.get("success") is True
        assert "job_id" in result

    def test_job_id_is_unique(self) -> None:
        r1 = json.loads(
            image_generate_background_handler({"prompt": "Test 1"})
        )
        r2 = json.loads(
            image_generate_background_handler({"prompt": "Test 2"})
        )
        assert r1["job_id"] != r2["job_id"]


class TestBackgroundStatusHandler:
    """Tests for background status handler."""

    def test_missing_job_id_returns_error(self) -> None:
        result = json.loads(
            image_generate_background_status_handler({"job_id": ""})
        )
        assert result.get("success") is False
        assert "job_id is required" in result.get("error", "")

    def test_unknown_job_returns_error(self) -> None:
        result = json.loads(
            image_generate_background_status_handler({"job_id": "nonexistent"})
        )
        assert result.get("success") is False
        assert "not found" in result.get("error", "")

    @patch("abacus_ai.background._jobs_dir")
    def test_known_job_returns_status(
        self, mock_jobs_dir
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            job_dir = Path(tmpdir) / "test-job-123"
            job_dir.mkdir(parents=True)
            status_path = job_dir / "status.json"
            status_path.write_text(
                json.dumps({"job_id": "test-job-123", "status": "completed"}),
                encoding="utf-8",
            )
            mock_jobs_dir.return_value = Path(tmpdir)

            result = json.loads(
                image_generate_background_status_handler(
                    {"job_id": "test-job-123"}
                )
            )
            assert result.get("success") is True
            assert result.get("status") == "completed"
