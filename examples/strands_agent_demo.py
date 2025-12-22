"""
Example: Using use_spot with Strands Agent

This demonstrates how to integrate use_spot with a Strands agent.
"""

import os
from strands import Agent
from strands.models.bedrock import BedrockModel

# Import use_spot tool with Strands decorator
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from use_spot_strands import use_spot


def main():
    # Check credentials
    if not os.getenv("SPOT_USERNAME") or not os.getenv("SPOT_PASSWORD"):
        print("❌ Set SPOT_USERNAME and SPOT_PASSWORD environment variables")
        sys.exit(1)

    hostname = os.getenv("SPOT_HOSTNAME", "192.168.80.3")

    print(f"🦆 Strands Agent with Spot Control")
    print(f"   Robot: {hostname}")
    print("=" * 50)

    # Create Strands agent with use_spot tool
    model = BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
        params={"temperature": 1.0, "max_tokens": 10000},
    )

    agent = Agent(
        model=model,
        tools=[use_spot],
        system_prompt=f"""You are a robotic control assistant with access to a Boston Dynamics Spot robot.

Robot Details:
- Hostname: {hostname}
- Available via use_spot tool

Your capabilities:
- Control robot movement (stand, sit, walk)
- Capture images from cameras
- Query robot state
- Manage power

Use the use_spot tool with service-method pattern:
- service: robot_command, robot_state, power, image, etc.
- method: stand, sit, get_robot_state, get_image_from_sources, etc.
- params: method-specific parameters

Always check response status before proceeding.
Be safe and deliberate with robot control commands.
""",
    )

    # Example 1: Ask agent to check robot status
    print("\n📝 Query 1: 'What is the robot's current state?'")
    print("-" * 50)
    response = agent("What is the robot's current state?")
    print(response)

    # Example 2: Ask agent to capture an image
    print("\n📝 Query 2: 'Capture an image from the front left camera'")
    print("-" * 50)
    response = agent("Capture an image from the front left camera")
    print(response)

    # Example 3: More complex task
    print(
        "\n📝 Query 3: 'Check if the robot is powered on, and if not, list what we would need to do'"
    )
    print("-" * 50)
    response = agent("Check if the robot is powered on, and if not, list what we would need to do")
    print(response)

    print("\n" + "=" * 50)
    print("✅ Strands agent demo completed!")


if __name__ == "__main__":
    main()
