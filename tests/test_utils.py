"""Tests for utility functions."""

from __future__ import annotations

from pathlib import Path

import pytest

from abacus_ai.utils import detect_image_format, strip_data_url_prefix, to_image_url_part


class TestDetectImageFormat:
    """Tests for ``detect_image_format``."""

    def test_png(self) -> None:
        result = detect_image_format("data:image/png;base64,abc123")
        assert result == "png"

    def test_jpeg(self) -> None:
        result = detect_image_format("data:image/jpeg;base64,abc123")
        assert result == "jpg"

    def test_jpg(self) -> None:
        result = detect_image_format("data:image/jpg;base64,abc123")
        assert result == "jpg"

    def test_webp(self) -> None:
        result = detect_image_format("data:image/webp;base64,abc123")
        assert result == "webp"

    def test_gif(self) -> None:
        result = detect_image_format("data:image/gif;base64,abc123")
        assert result == "gif"

    def test_no_match(self) -> None:
        result = detect_image_format("not a data URL")
        assert result == "png"

    def test_empty(self) -> None:
        result = detect_image_format("")
        assert result == "png"


class TestStripDataUrlPrefix:
    """Tests for ``strip_data_url_prefix``."""

    def test_with_base64(self) -> None:
        result = strip_data_url_prefix("data:image/png;base64,abc123")
        assert result == "abc123"

    def test_no_base64(self) -> None:
        result = strip_data_url_prefix("not a valid url")
        assert result == "not a valid url"

    def test_empty(self) -> None:
        result = strip_data_url_prefix("")
        assert result == ""


class TestToImageUrlPart:
    """Tests for ``to_image_url_part``."""

    def test_empty(self) -> None:
        result = to_image_url_part("")
        assert result is None

    def test_none(self) -> None:
        result = to_image_url_part(None)  # type: ignore
        assert result is None

    def test_https_url_passthrough(self) -> None:
        url = "https://example.com/image.png"
        result = to_image_url_part(url)
        assert result == url

    def test_data_url_passthrough(self) -> None:
        url = "data:image/png;base64,abc123"
        result = to_image_url_part(url)
        assert result == url

    def test_missing_file(self) -> None:
        result = to_image_url_part("/nonexistent/path/image.png")
        assert result is None
