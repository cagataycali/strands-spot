"""
Basic usage example for use_spot tool

This example demonstrates basic robot control operations:
1. Get robot state (check if operational)
2. Power on the robot
3. Stand up
4. Capture an image
5. Sit down
6. Power off

Prerequisites:
- Spot robot on network
- Set environment variables:
  export SPOT_HOSTNAME="192.168.80.3"
  export SPOT_USERNAME="admin"
  export SPOT_PASSWORD="password"
"""

import os
import sys
import time

# Add tools to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from use_spot import use_spot


def main():
    # Load from environment
    hostname = os.getenv("SPOT_HOSTNAME", "192.168.80.3")
    username = os.getenv("SPOT_USERNAME")
    password = os.getenv("SPOT_PASSWORD")

    if not username or not password:
        print("❌ Error: Set SPOT_USERNAME and SPOT_PASSWORD environment variables")
        sys.exit(1)

    print(f"🦆 Connecting to Spot at {hostname}...")
    print("-" * 50)

    # Step 1: Get robot state (no lease required)
    print("\n1️⃣ Getting robot state...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="robot_state",
        method="get_robot_state",
        params={},
    )

    if result["status"] == "error":
        print(f"❌ Failed: {result['content'][0]['text']}")
        sys.exit(1)

    print(f"✅ {result['content'][0]['text']}")
    # Extract response data from JSON block
    if len(result["content"]) > 1 and "json" in result["content"][1]:
        response_data = result["content"][1]["json"]["response_data"]
        power_state = response_data.get("power_state", {})
        print(f"   Power state: {power_state.get('motor_power_state', 'unknown')}")

    # Step 2: Power on
    print("\n2️⃣ Powering on robot...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="power",
        method="power_on",
        params={"timeout_sec": 20},
    )

    if result["status"] == "error":
        print(f"❌ Failed: {result['content'][0]['text']}")
        sys.exit(1)

    print(f"✅ {result['content'][0]['text']}")

    # Step 3: Stand up
    print("\n3️⃣ Standing up...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="robot_command",
        method="stand",
        params={},
    )

    if result["status"] == "error":
        print(f"❌ Failed: {result['content'][0]['text']}")
        sys.exit(1)

    print(f"✅ {result['content'][0]['text']}")
    time.sleep(3)  # Give robot time to stand

    # Step 4: Capture image
    print("\n4️⃣ Capturing image from front left camera...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="image",
        method="get_image_from_sources",
        params={"image_sources": ["frontleft_fisheye_image"]},
    )

    if result["status"] == "error":
        print(f"❌ Failed: {result['content'][0]['text']}")
    else:
        print(f"✅ {result['content'][0]['text']}")
        # Note: Image data is in result['content'][1]['json']['response_data']

    # Step 5: Sit down
    print("\n5️⃣ Sitting down...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="robot_command",
        method="sit",
        params={},
    )

    if result["status"] == "error":
        print(f"❌ Failed: {result['content'][0]['text']}")
    else:
        print(f"✅ {result['content'][0]['text']}")
        time.sleep(3)  # Give robot time to sit

    # Step 6: Power off
    print("\n6️⃣ Powering off...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="power",
        method="power_off",
        params={"cut_immediately": False, "timeout_sec": 20},
    )

    if result["status"] == "error":
        print(f"❌ Failed: {result['content'][0]['text']}")
    else:
        print(f"✅ {result['content'][0]['text']}")

    print("\n" + "=" * 50)
    print("✅ Basic control sequence completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()
