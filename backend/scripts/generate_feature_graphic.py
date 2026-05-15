"""Generate the Play Store feature graphic (1024×500 banner shown at the top of
the store listing) for HuatPick."""
import asyncio
import base64
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from emergentintegrations.llm.chat import LlmChat, UserMessage  # noqa: E402

PROMPT = """A Play Store feature graphic for an Android app called "HuatPick" — Malaysia lottery prediction app. Banner aspect ratio (wide rectangle, roughly 2:1, around 1024 wide by 500 tall).

Layout: split horizontally.
  LEFT (60% width): pure white background. The bold word "HuatPick" rendered in a clean modern sans-serif typeface (Manrope, weight 800), black color (#0A0A0A). Below it in smaller text: "Lucky numbers, picked smart." in medium gray. To the left of the title, a small solid red circle (#DC2626) with a white "8" inside it (matching the app icon).
  RIGHT (40% width): A clean abstract illustration on white background. Three large red filled circles in a vertical row, each containing a different big white bold digit ("8", "2", "8"). Crisp flat colors, no gradients, no shadows, plenty of white space around them. Swiss-minimalist style.

Style rules:
- White background everywhere
- Two colors only: red #DC2626 and black/dark gray for text
- No textures, no gradients, no shadows, no noise
- Generous whitespace
- Premium banking-app / fintech aesthetic
- Crisp vector-clean edges
- High resolution, banner aspect ratio 2:1 (1024x500)
- No other text besides "HuatPick" and the tagline
- No people, no hands, no money imagery"""


async def main():
    chat = (
        LlmChat(
            api_key=os.environ["EMERGENT_LLM_KEY"],
            session_id="huatpick-feature-graphic",
            system_message="You are an expert Play Store / App Store marketing-asset designer.",
        )
        .with_model("gemini", "gemini-3.1-flash-image-preview")
        .with_params(modalities=["image", "text"])
    )
    text, images = await chat.send_message_multimodal_response(UserMessage(text=PROMPT))
    print("model reply:", (text or "")[:200])
    if not images:
        print("ERROR no images")
        return
    out = Path("/app/frontend/assets/feature-graphic.png")
    out.write_bytes(base64.b64decode(images[0]["data"]))
    print(f"saved {out}")


if __name__ == "__main__":
    asyncio.run(main())
