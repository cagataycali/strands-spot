"""
Velocity control example for use_spot tool

Demonstrates basic robot movement using velocity commands.
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from use_spot import use_spot


def main():
    hostname = os.getenv("SPOT_HOSTNAME", "192.168.80.3")
    username = os.getenv("SPOT_USERNAME")
    password = os.getenv("SPOT_PASSWORD")

    if not username or not password:
        print("❌ Set SPOT_USERNAME and SPOT_PASSWORD")
        sys.exit(1)

    print(f"🦆 Velocity Control Demo - Spot at {hostname}")
    print("=" * 50)

    # Power on
    print("\n⚡ Powering on...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="power",
        method="power_on",
        params={"timeout_sec": 20},
    )
    if result["status"] == "error":
        print(f"❌ {result['content'][0]['text']}")
        sys.exit(1)
    print("✅ Powered on")

    # Stand
    print("\n🦿 Standing up...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="robot_command",
        method="stand",
        params={},
    )
    if result["status"] == "error":
        print(f"❌ {result['content'][0]['text']}")
        sys.exit(1)
    print("✅ Standing")
    time.sleep(3)

    # Walk forward
    print("\n➡️  Walking forward (0.5 m/s for 3 seconds)...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="robot_command",
        method="velocity_command",
        params={"v_x": 0.5, "v_y": 0.0, "v_rot": 0.0},
    )
    print(f"✅ {result['content'][0]['text']}")
    time.sleep(3)

    # Stop
    print("\n🛑 Stopping...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="robot_command",
        method="velocity_command",
        params={"v_x": 0.0, "v_y": 0.0, "v_rot": 0.0},
    )
    print(f"✅ {result['content'][0]['text']}")
    time.sleep(1)

    # Turn in place
    print("\n🔄 Rotating in place (0.3 rad/s for 3 seconds)...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="robot_command",
        method="velocity_command",
        params={"v_x": 0.0, "v_y": 0.0, "v_rot": 0.3},
    )
    print(f"✅ {result['content'][0]['text']}")
    time.sleep(3)

    # Stop
    print("\n🛑 Stopping...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="robot_command",
        method="velocity_command",
        params={"v_x": 0.0, "v_y": 0.0, "v_rot": 0.0},
    )
    print(f"✅ {result['content'][0]['text']}")
    time.sleep(1)

    # Walk sideways
    print("\n⬅️  Walking sideways left (0.3 m/s for 2 seconds)...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="robot_command",
        method="velocity_command",
        params={"v_x": 0.0, "v_y": 0.3, "v_rot": 0.0},
    )
    print(f"✅ {result['content'][0]['text']}")
    time.sleep(2)

    # Stop
    print("\n🛑 Stopping...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="robot_command",
        method="velocity_command",
        params={"v_x": 0.0, "v_y": 0.0, "v_rot": 0.0},
    )
    print(f"✅ {result['content'][0]['text']}")

    # Sit
    print("\n💺 Sitting down...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="robot_command",
        method="sit",
        params={},
    )
    if result["status"] == "success":
        print("✅ Sitting")
    time.sleep(3)

    # Power off
    print("\n⚡ Powering off...")
    result = use_spot(
        hostname=hostname,
        username=username,
        password=password,
        service="power",
        method="power_off",
        params={"cut_immediately": False, "timeout_sec": 20},
    )
    if result["status"] == "success":
        print("✅ Powered off")

    print("\n" + "=" * 50)
    print("✅ Velocity control demo completed!")


if __name__ == "__main__":
    main()
