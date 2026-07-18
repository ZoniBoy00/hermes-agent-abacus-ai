"""Tests for the AbacusAIImageProvider."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from abacus_ai.models import (
    MODEL_CATALOG,
    DEFAULT_MODEL,
    resolve_aspect_ratio_for_model,
)
from abacus_ai.config import resolve_credentials


# ------------------------------------------------------------------
# Model & configuration tests
# ------------------------------------------------------------------


class TestModels:
    """Tests for model catalog and defaults."""

    def test_default_model(self) -> None:
        assert DEFAULT_MODEL == "flux2_pro"

    def test_model_catalog_not_empty(self) -> None:
        assert len(MODEL_CATALOG) > 0

    def test_model_catalog_has_required_keys(self) -> None:
        for entry in MODEL_CATALOG:
            assert "id" in entry
            assert "display" in entry
            assert "strengths" in entry

    def test_model_catalog_includes_nano_banana_pro(self) -> None:
        ids = [m["id"] for m in MODEL_CATALOG]
        assert "nano_banana_pro" in ids

    def test_model_catalog_includes_flux2_pro(self) -> None:
        ids = [m["id"] for m in MODEL_CATALOG]
        assert "flux2_pro" in ids


class TestAspectRatioResolution:
    """Tests for model-specific aspect ratio resolution."""

    def test_flux_landscape(self) -> None:
        result = resolve_aspect_ratio_for_model("landscape", "flux2_pro")
        assert result == "landscape_16_9"

    def test_flux_square(self) -> None:
        result = resolve_aspect_ratio_for_model("square", "flux2_pro")
        assert result == "square_hd"

    def test_flux_portrait(self) -> None:
        result = resolve_aspect_ratio_for_model("portrait", "flux2_pro")
        assert result == "portrait_16_9"

    def test_midjourney_square(self) -> None:
        result = resolve_aspect_ratio_for_model("square", "midjourney")
        assert result == "1:1"

    def test_midjourney_landscape(self) -> None:
        result = resolve_aspect_ratio_for_model("landscape", "midjourney")
        assert result == "16:9"

    def test_dalle_square(self) -> None:
        result = resolve_aspect_ratio_for_model("square", "dalle")
        assert result == "1:1"

    def test_flux_pro_ultra_landscape(self) -> None:
        result = resolve_aspect_ratio_for_model("landscape", "flux_pro_ultra")
        assert result == "16:9"

    def test_nano_banana_flux_format(self) -> None:
        """nano_banana_pro uses FLUX format (not in STANDARD set)."""
        result = resolve_aspect_ratio_for_model("landscape", "nano_banana_pro")
        assert result == "landscape_16_9"


@pytest.mark.skipif(
    True,
    reason="Hermes core not available in standalone test",
)
class TestCredentials:
    """Tests for credential resolution (require Hermes config)."""

    def test_no_credentials_returns_empty(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            "hermes_cli.config.load_config",
            lambda: {},
        )
        monkeypatch.delenv("ABACUS_AI_API_KEY", raising=False)
        monkeypatch.delenv("HONCHO_API_KEY", raising=False)
        base_url, api_key = resolve_credentials()
        assert api_key == ""
        assert base_url == ""

    def test_with_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            "hermes_cli.config.load_config",
            lambda: {},
        )
        monkeypatch.setenv("ABACUS_AI_API_KEY", "test-key-456")
        base_url, api_key = resolve_credentials()
        assert api_key == "test-key-456"
        assert "routellm" in base_url


# ------------------------------------------------------------------
# Provider tests (require Hermes core)
# ------------------------------------------------------------------


@pytest.mark.skipif(
    True,
    reason="Hermes core not available in standalone test",
)
class TestProviderIntegration:
    """Placeholder for Hermes-integrated provider tests.

    These require the full Hermes environment (ImageGenProvider ABC,
    save_b64_image, etc.). Run with Hermes' test suite.
    """

    def test_placeholder(self) -> None:
        pass
