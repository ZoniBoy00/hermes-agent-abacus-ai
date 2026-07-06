# Abacus AI Image Generation Plugin for Hermes Agent

**Version 2.0.0** — [![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> ⚡ Generate high-quality images directly in [Hermes Agent](https://hermes-agent.nousresearch.com) using [Abacus AI's RouteLLM API](https://abacus.ai/help/developer-platform/route-llm). Supports FLUX 2 Pro, Nano Banana Pro (up to 4K), DALL-E, MidJourney, and 20+ models.

## Features

- 🎨 **20+ Image Models** — FLUX 2 Pro, FLUX Pro Ultra, Nano Banana Pro (4K), MidJourney, DALL-E, and more
- ⚡ **Native `image_gen` Provider** — Works as a first-class Hermes image generation backend
- 🖼️ **Up to 4K Resolution** — Nano Banana Pro supports `1080p`, `2K`, `4K`
- 🔄 **Text-to-Image & Image-to-Image** — Generate from prompts or edit existing images
- ⏳ **Background Generation** — Run image generation asynchronously and poll for results
- 💰 **Cost-Effective** — Uses your existing Abacus AI ChatLLM subscription credits
- 🎯 **Multi-Platform** — Works in Telegram, Discord, CLI, and all Hermes surfaces
- 📦 **Modular Code** — Clean separation into provider, config, models, utils, and background modules
- ✅ **Tested** — 37+ unit tests covering utilities, credentials, models, and background jobs

## Prerequisites

- [Hermes Agent](https://hermes-agent.nousresearch.com) installed and running
- An [Abacus AI](https://abacus.ai) account with ChatLLM subscription
- Your RouteLLM API key from [abacus.ai/app/route-llm-apis](https://abacus.ai/app/route-llm-apis)

## Installation

### Option 1: Install via Hermes Agent (recommended)

Copy and paste this prompt to your Hermes Agent (Telegram, Discord, or CLI). It will clone the repo, copy the files, configure everything, and restart the gateway automatically:

> Install the Abacus AI image generation plugin v2.0.0 from the public GitHub repo https://github.com/ZoniBoy00/hermes-agent-abacus-ai. Clone the repo to /tmp, copy the abacus_ai/ directory to ~/.hermes/plugins/image_gen/abacus_ai/, enable image_gen/abacus_ai in plugins.enabled in config.yaml, set image_gen.provider to abacus_ai, configure custom_providers with name abacus-ai using my API key, then restart the gateway.

Make sure you have your [Abacus AI RouteLLM API key](https://abacus.ai/app/route-llm-apis) ready — Hermes will ask for it during installation.

### Option 2: Manual Install

1. Clone the repository:

```bash
git clone https://github.com/ZoniBoy00/hermes-agent-abacus-ai.git /tmp/hermes-agent-abacus-ai
```

2. Copy the `abacus_ai/` directory to your Hermes image_gen plugins folder:

```bash
cp -r /tmp/hermes-agent-abacus-ai/abacus_ai ~/.hermes/plugins/image_gen/abacus_ai/
```

3. Enable the plugin in `~/.hermes/config.yaml`:

```yaml
plugins:
  enabled:
    - image_gen/abacus_ai
```

4. Set the image generation provider:

```bash
hermes config set image_gen.provider abacus_ai
```

5. Configure your Abacus AI API key:

```yaml
custom_providers:
  - name: abacus-ai
    api_key: "your-api-key-here"
    base_url: "https://routellm.abacus.ai/v1"
```

6. Restart the Hermes gateway:

```bash
systemctl --user restart hermes-gateway
```

### Option 3: Install via pip

```bash
pip install git+https://github.com/ZoniBoy00/hermes-agent-abacus-ai.git
```

Then enable the plugin in `~/.hermes/config.yaml` and restart.

### Cleanup (optional)

```bash
rm -rf /tmp/hermes-agent-abacus-ai
```

## Plugin Structure

```
abacus_ai/
├── __init__.py       # Plugin registration (register provider + background tools)
├── provider.py       # ImageGenProvider implementation (generate, extract)
├── config.py         # Credential and config resolution
├── models.py         # Model catalog and aspect ratio helpers
├── utils.py          # Image URL conversion and format detection
├── background.py     # Background image generation (async jobs)
└── plugin.yaml       # Plugin manifest (kind: backend)
tests/
├── __init__.py
├── conftest.py       # Test fixtures and mocks
├── test_utils.py     # Utility function tests
├── test_provider.py  # Model, credential, and aspect ratio tests
└── test_background.py # Background job tests
```

## Background Generation

In addition to synchronous image generation, the plugin provides two background tools:

### `image_generate_background`

Start an image generation job that runs in the background. Returns immediately with a `job_id`.

- Supports single prompts and batch mode (multiple jobs via `jobs` array)
- Job state is persisted to `$HERMES_HOME/cache/abacus_ai_jobs/<job_id>/`

### `image_generate_background_status`

Poll for the result of a background job:

- Returns `"status": "running"` while the job is in progress
- Returns `"status": "completed"` with the result when done
- Returns `"status": "failed"` on error

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ABACUS_AI_API_KEY` | Your Abacus AI RouteLLM API key | — |
| `ABACUS_AI_BASE_URL` | API base URL | `https://routellm.abacus.ai/v1` |
| `ABACUS_AI_IMAGE_MODEL` | Default image model override | `flux2_pro` |

### Config File

```yaml
image_gen:
  provider: abacus_ai
  abacus_ai:
    model: flux2_pro  # default model
```

## Available Models

| Model ID | Display Name | Best For |
|----------|-------------|----------|
| `nano_banana_pro` | Nano Banana Pro | Highest resolution (up to 4K), Google DeepMind |
| `flux_pro_ultra` | FLUX Pro Ultra | Highest quality, photorealistic |
| `flux2_pro` | FLUX 2 Pro | High quality, photorealistic (default) |
| `flux2` | FLUX 2 | Fast, good quality |
| `midjourney` | MidJourney | Artistic, stylistic |
| `dalle` | DALL-E | Creative, strong prompt adherence |

## Usage

Once installed and configured, Hermes will use the Abacus AI provider automatically when generating images. Simply ask Hermes to create an image — the `image_generate` tool will use this provider by default.

### Telegram / Discord

```
Generate an image of a cyberpunk city at night, neon lights, futuristic
Make a photorealistic render of a wooden cabin in the mountains
Create a digital art portrait of a wolf with glowing eyes
Generate a 4K image of northern lights — use Nano Banana Pro
```

### CLI

```bash
hermes chat -q "Generate a beautiful landscape painting of northern lights over a lake"
```

## Supported Parameters

The provider supports these optional `image_config` parameters:

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `num_images` | integer | Number of images to generate (1-4) | `1` |
| `quality` | string | Quality tier (`low`, `medium`, `high`) | model-dependent |
| `resolution` | string | Output resolution: `1080p`, `2K`, or `4K`. Only works with `nano_banana_pro` model. Leave unset for model's default resolution. | not set (model default) |
| `rewrite_prompt` | boolean | Auto-improve prompts for better results | `true` |

## Changelog

### v2.0.0
- Modular code structure (provider.py, config.py, models.py, utils.py, background.py)
- Background image generation (`image_generate_background` + `_status`)
- Nano Banana Pro support with up to 4K resolution
- Unit test suite (37+ tests)
- pip install support via pyproject.toml
- Improved error handling and response parsing

### v1.1.0
- Rich `requires_env` format in plugin.yaml
- Model-specific aspect ratio resolution
- Image format detection (PNG, JPEG, WebP)

### v1.0.0
- Initial release with Abacus AI image generation
- FLUX 2 Pro, DALL-E, MidJourney support

## Credits & License

Built for [Hermes Agent](https://hermes-agent.nousresearch.com) by ZoniBoy00.

- **Author:** ZoniBoy00
- **License:** MIT
- **Repository:** [ZoniBoy00/hermes-agent-abacus-ai](https://github.com/ZoniBoy00/hermes-agent-abacus-ai)

## Support

- [Abacus AI RouteLLM Docs](https://abacus.ai/help/developer-platform/route-llm)
- [Hermes Agent Docs](https://hermes-agent.nousresearch.com/docs)
- [Abacus AI API Keys](https://abacus.ai/app/route-llm-apis)
