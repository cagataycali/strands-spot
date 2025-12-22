#!/usr/bin/env python3
"""
Quick test script to verify use_spot tool works

This script performs a minimal connection test without moving the robot.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))


def test_connection():
    """Test basic connection and authentication"""
    from use_spot import use_spot

    hostname = os.getenv("SPOT_HOSTNAME", "192.168.80.3")
    username = os.getenv("SPOT_USERNAME")
    password = os.getenv("SPOT_PASSWORD")

    if not username or not password:
        print("❌ Set SPOT_USERNAME and SPOT_PASSWORD")
        print("\nExample:")
        print('  export SPOT_HOSTNAME="192.168.80.3"')
        print('  export SPOT_USERNAME="admin"')
        print('  export SPOT_PASSWORD="password"')
        sys.exit(1)

    print(f"🦆 Testing connection to Spot at {hostname}...")
    print("-" * 50)

    # Test 1: Get robot state (safest test)
    print("\n1️⃣ Testing robot_state service...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="robot_state",
        method="get_robot_state",
        params={},
    )

    if result["status"] == "success":
        print(f"✅ {result['content'][0]['text']}")
        print(f"   Duration: {result['metadata']['duration_ms']}ms")

        # Show some basic info
        data = result.get("data", {})
        power_state = data.get("power_state", {})
        print(f"   Motor power: {power_state.get('motor_power_state', 'unknown')}")
        print(f"   Shore power: {power_state.get('shore_power_state', 'unknown')}")
    else:
        print(f"❌ {result['content'][0]['text']}")
        sys.exit(1)

    # Test 2: List image sources
    print("\n2️⃣ Testing image service...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="image",
        method="list_image_sources",
        params={},
    )

    if result["status"] == "success":
        print(f"✅ {result['content'][0]['text']}")
        sources = result["data"].get("image_sources", [])
        print(f"   Available cameras: {len(sources)}")
    else:
        print(f"❌ {result['content'][0]['text']}")

    # Test 3: List services (directory service)
    print("\n3️⃣ Testing directory service...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="directory",
        method="list",
        params={},
    )

    if result["status"] == "success":
        print(f"✅ {result['content'][0]['text']}")
        # Note: Service list would be in result['data']
    else:
        print(f"❌ {result['content'][0]['text']}")

    print("\n" + "=" * 50)
    print("✅ Connection test passed!")
    print("\nYou can now run full examples:")
    print("  python examples/basic_control.py")
    print("  python examples/image_capture.py")
    print("  python examples/velocity_control.py")


if __name__ == "__main__":
    test_connection()
