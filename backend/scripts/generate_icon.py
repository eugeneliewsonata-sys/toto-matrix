"""One-time script: generate the HuatPick app icon using Gemini Nano Banana.

Usage:
    cd /app/backend && python scripts/generate_icon.py

Outputs:
    /app/frontend/assets/icon.png
"""
import asyncio
import base64
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from emergentintegrations.llm.chat import LlmChat, UserMessage  # noqa: E402

PROMPT = """An app icon design for a mobile app called "HuatPick" — a Malaysia lottery number prediction app. Swiss-minimalist style, Apple App Store quality.

Design: a perfectly centered, bold, solid filled circle in vivid red (hex #DC2626) on a pure white square background. Inside the red circle is the bold white digit "8" (the luckiest number in Chinese / Malaysian culture), drawn in a clean modern sans-serif typeface (Manrope-style, weight 800). The digit fills about 55% of the circle. The circle fills about 70% of the canvas, leaving generous white margin (Apple-style padding).

Style rules:
- No text, no letters other than the digit "8"
- No gradients, no inner shadows, no outer shadows
- No textures, no patterns, no noise
- Crisp flat colors only (red #DC2626, white #FFFFFF)
- Perfect 1:1 aspect ratio, 1024x1024 pixels
- Print-quality vector-clean edges
- Premium fintech / banking app aesthetic
- The icon should look great both small (48px) and large (1024px)"""


async def main():
    api_key = os.environ["EMERGENT_LLM_KEY"]
    chat = (
        LlmChat(
            api_key=api_key,
            session_id="huatpick-icon-gen",
            system_message="You are an expert mobile app icon designer producing premium iOS/Android icons.",
        )
        .with_model("gemini", "gemini-3.1-flash-image-preview")
        .with_params(modalities=["image", "text"])
    )

    out_dir = Path("/app/frontend/assets")
    out_dir.mkdir(parents=True, exist_ok=True)

    text, images = await chat.send_message_multimodal_response(UserMessage(text=PROMPT))
    print("Model text reply:", (text or "")[:200])
    if not images:
        print("ERROR: no images returned")
        sys.exit(1)

    img = images[0]
    print(f"Got image: mime={img.get('mime_type')} bytes_len_b64={len(img['data'])}")
    out_path = out_dir / "icon.png"
    out_path.write_bytes(base64.b64decode(img["data"]))
    print(f"✓ Saved {out_path}")
    print(f"  size: {out_path.stat().st_size} bytes")


if __name__ == "__main__":
    asyncio.run(main())
