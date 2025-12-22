"""
Image capture example for use_spot tool

Demonstrates capturing images from multiple cameras on Spot.
"""

import os
import sys
import base64
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from use_spot import use_spot


def save_image(image_data: bytes, filename: str):
    """Save image bytes to file"""
    output_dir = Path("./spot_images")
    output_dir.mkdir(exist_ok=True)

    filepath = output_dir / filename
    with open(filepath, "wb") as f:
        f.write(image_data)

    print(f"   💾 Saved to: {filepath}")


def main():
    hostname = os.getenv("SPOT_HOSTNAME", "192.168.80.3")
    username = os.getenv("SPOT_USERNAME")
    password = os.getenv("SPOT_PASSWORD")

    if not username or not password:
        print("❌ Set SPOT_USERNAME and SPOT_PASSWORD")
        sys.exit(1)

    print(f"🦆 Image Capture Demo - Spot at {hostname}")
    print("=" * 50)

    # List available image sources
    print("\n📷 Listing available cameras...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="image",
        method="list_image_sources",
        params={},
    )

    if result["status"] == "success":
        sources = result["data"].get("image_sources", [])
        print(f"✅ Found {len(sources)} cameras:")
        for source in sources:
            print(f"   • {source.get('name', 'unknown')}")
    else:
        print(f"❌ {result['content'][0]['text']}")
        sys.exit(1)

    # Capture from front cameras
    print("\n📸 Capturing from front left camera...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="image",
        method="get_image_from_sources",
        params={"image_sources": ["frontleft_fisheye_image"]},
    )

    if result["status"] == "success":
        print(f"✅ {result['content'][0]['text']}")
        # Note: Image data would be in result['data']
        # In real implementation, save image to file
    else:
        print(f"❌ {result['content'][0]['text']}")

    # Capture from multiple cameras
    print("\n📸 Capturing from multiple cameras...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="image",
        method="get_image_from_sources",
        params={
            "image_sources": [
                "frontleft_fisheye_image",
                "frontright_fisheye_image",
                "hand_color_image",
            ]
        },
    )

    if result["status"] == "success":
        print(f"✅ {result['content'][0]['text']}")
        print(f"   Captured {len(result['data'].get('image_responses', []))} images")
    else:
        print(f"❌ {result['content'][0]['text']}")

    print("\n" + "=" * 50)
    print("✅ Image capture demo completed!")


if __name__ == "__main__":
    main()
