<div align="center">
  <div>
    <a href="https://strandsagents.com">
      <img src="https://strandsagents.com/latest/assets/logo-github.svg" alt="Strands Agents" width="55px" height="105px">
    </a>
  </div>

  <h1>
    Strands Spot
  </h1>

  <h2>
    Boston Dynamics Spot Control for Strands Agents
  </h2>

  <div align="center">
    <a href="https://github.com/cagataycali/strands-spot"><img alt="GitHub stars" src="https://img.shields.io/github/stars/cagataycali/strands-spot"/></a>
    <a href="https://github.com/cagataycali/strands-spot/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/cagataycali/strands-spot"/></a>
    <a href="https://dev.bostondynamics.com"><img alt="Spot SDK" src="https://img.shields.io/badge/Spot_SDK-5.0+-yellow"/></a>
  </div>
  
  <p>
    <a href="https://strandsagents.com/">Strands Docs</a>
    ◆ <a href="https://dev.bostondynamics.com">Spot SDK Docs</a>
    ◆ <a href="https://github.com/boston-dynamics/spot-sdk">Spot SDK GitHub</a>
  </p>
</div>

A Python tool for controlling Boston Dynamics Spot robots through the [Strands Agents](https://github.com/strands-agents/sdk-python) framework.

Call Spot SDK services and methods directly without writing boilerplate connection code:

```python
use_spot(service="robot_command", method="stand")
use_spot(service="image", method="get_image_from_sources") 
use_spot(service="power", method="power_on")
```

Works with natural language when used with Strands agents:

```python
agent = Agent(tools=[use_spot])
agent("Make Spot stand up and take a picture")
```

## How It Works

You specify which Spot SDK service and method to call. The tool handles connections, authentication, and lease management:

```python
use_spot(
    service="robot_command",    # Which SDK service
    method="stand",              # Which method to call
    params={}                    # Method parameters
)
```

This maps to Spot SDK: `service="robot_command"` → `RobotCommandClient`, `method="stand"` → `synchro_stand_command()`

## Installation

```bash
pip install strands-spot
```

**Dependencies:**
```bash
pip install bosdyn-client bosdyn-api bosdyn-core  # Required
pip install strands-agents  # Optional, for natural language
```

**Environment setup:**
```bash
export SPOT_HOSTNAME="192.168.80.3"
export SPOT_USERNAME="admin"
export SPOT_PASSWORD="password"
```

## Usage

```python
from strands_spot import use_spot

# Stand the robot
use_spot(
    hostname="192.168.80.3",
    service="robot_command",
    method="stand"
)

# Capture image
use_spot(
    hostname="192.168.80.3",
    service="image",
    method="get_image_from_sources",
    params={"image_sources": ["frontleft_fisheye_image"]}
)

# With natural language
from strands import Agent
agent = Agent(tools=[use_spot])
agent("Make Spot stand and take a picture")
```

## Available Services

| Service | Client | Common Methods | Description |
|---------|--------|----------------|-------------|
| **robot_command** | RobotCommandClient | `stand`, `sit`, `velocity_command`, `self_right` | Motion control and poses |
| **robot_state** | RobotStateClient | `get_robot_state`, `get_robot_metrics`, `get_robot_hardware_configuration` | Query robot status |
| **power** | PowerClient | `power_on`, `power_off`, `power_cycle_robot` | Power management |
| **image** | ImageClient | `list_image_sources`, `get_image_from_sources` | Camera capture |
| **graph_nav** | GraphNavClient | `navigate_to`, `upload_graph`, `set_localization` | Autonomous navigation |
| **manipulation** | ManipulationApiClient | `manipulation_api_command`, `grasp_override` | Arm control |
| **docking** | DockingClient | `docking_command`, `get_docking_config` | Charging station docking |
| **lease** | LeaseClient | `acquire`, `release`, `list_leases` | Resource management |
| **estop** | EstopClient | `register`, `deregister`, `set_status` | Emergency stop |
| **time_sync** | TimeSyncClient | `get_robot_time_range`, `update` | Clock synchronization |
| **directory** | DirectoryClient | `list`, `get_entry` | Service discovery |
| **choreography** | ChoreographyClient | `execute_choreography`, `list_all_moves` | Dance routines |
| **data_acquisition** | DataAcquisitionClient | `acquire_data`, `list_capture_actions` | Sensor data collection |
| **autowalk** | AutowalkClient | `load_autowalk`, `compile_autowalk` | Mission playback |
| **spot_check** | SpotCheckClient | `start_spot_check`, `spot_check_feedback` | Robot diagnostics |

<details>
<summary><b>💡 100+ Methods Available</b></summary>

Each service exposes 5-20 methods. Examples:

**robot_command** (Motion Control):
- `stand`, `sit`, `self_right`, `safe_power_off`
- `velocity_command`, `trajectory_command`
- `arm_stow`, `arm_ready`, `gripper_command`
- `stance_command`, `follow_arm_command`

**robot_state** (Status Queries):
- `get_robot_state`, `get_robot_metrics`
- `get_robot_hardware_configuration`
- `get_hardware_status_streaming`

**image** (Vision):
- `list_image_sources`, `get_image_from_sources`
- `build_image_request`, `decode_image`

**graph_nav** (Navigation):
- `navigate_to`, `navigate_route`, `navigate_to_anchor`
- `upload_graph`, `download_graph`
- `set_localization`, `get_localization_state`
- `clear_graph`, `get_status`

See [Spot SDK Python Client Reference](https://dev.bostondynamics.com/python/bosdyn-client/index.html) for complete method documentation.

</details>

## Features

**Automatic lease management** - Leases are acquired and released automatically

**Vision model integration** - Captured images are formatted for LLM vision models to analyze

**All SDK parameters exposed** - Full access to Spot SDK without limitations

```python
# Images captured from Spot can be analyzed by vision models
agent = Agent(tools=[use_spot])
agent("Take a picture and describe what you see")
```

## Examples

### Complete Workflow: Power → Stand → Capture → Sit → Power Off

```python
from strands_spot import use_spot

hostname = "192.168.80.3"
username = "admin"
password = "password"

# 1. Power on motors
use_spot(
    hostname=hostname, username=username, password=password,
    service="power", method="power_on", params={"timeout_sec": 20}
)

# 2. Stand up
use_spot(
    hostname=hostname, username=username, password=password,
    service="robot_command", method="stand", params={}
)

# 3. Capture image from front-left camera
result = use_spot(
    hostname=hostname, username=username, password=password,
    service="image", method="get_image_from_sources",
    params={"image_sources": ["frontleft_fisheye_image"]}
)

# 4. Sit down
use_spot(
    hostname=hostname, username=username, password=password,
    service="robot_command", method="sit", params={}
)

# 5. Power off
use_spot(
    hostname=hostname, username=username, password=password,
    service="power", method="power_off",
    params={"cut_immediately": False, "timeout_sec": 20}
)
```

### Velocity Control (Walking)

```python
import time

# Walk forward at 0.5 m/s
use_spot(
    service="robot_command",
    method="velocity_command",
    params={"v_x": 0.5, "v_y": 0.0, "v_rot": 0.0}
)
time.sleep(3)  # Walk for 3 seconds

# Turn in place at 0.3 rad/s
use_spot(
    service="robot_command",
    method="velocity_command",
    params={"v_x": 0.0, "v_y": 0.0, "v_rot": 0.3}
)
time.sleep(2)  # Turn for 2 seconds

# Stop
use_spot(
    service="robot_command",
    method="velocity_command",
    params={"v_x": 0.0, "v_y": 0.0, "v_rot": 0.0}
)
```

### Arm Manipulation

```python
# Unstow the arm
use_spot(service="robot_command", method="arm_ready", params={})

# Move arm to position (Cartesian command)
use_spot(
    service="manipulation",
    method="manipulation_api_command",
    params={
        "arm_cartesian_command": {
            "pose": {
                "position": {"x": 0.8, "y": 0.0, "z": 0.25},
                "rotation": {"w": 1, "x": 0, "y": 0, "z": 0}
            }
        }
    }
)

# Close gripper
use_spot(
    service="robot_command",
    method="gripper_command",
    params={
        "claw_gripper_command": {
            "trajectory": {"position": 0.0}  # 0.0 = fully closed
        }
    }
)

# Stow the arm
use_spot(service="robot_command", method="arm_stow", params={})
```

### Multi-Camera Capture

```python
# List all available cameras
result = use_spot(service="image", method="list_image_sources", params={})
print(result["content"][1]["json"]["response_data"]["image_sources"])

# Capture from multiple cameras simultaneously
result = use_spot(
    service="image",
    method="get_image_from_sources",
    params={
        "image_sources": [
            "frontleft_fisheye_image",
            "frontright_fisheye_image",
            "hand_color_image"
        ]
    }
)

# Images are automatically formatted for LLM consumption!
# The response content contains image blocks that the LLM can "see"
# Content structure:
# [
#   {"text": "✅ Executed image.get_image_from_sources - captured 3 image(s)"},
#   {"image": {"format": "jpeg", "source": {"bytes": <image1_bytes>}}},
#   {"image": {"format": "jpeg", "source": {"bytes": <image2_bytes>}}},
#   {"image": {"format": "jpeg", "source": {"bytes": <image3_bytes>}}},
#   {"json": {"response_data": {...}}},
#   {"json": {"metadata": {...}}}
# ]

# To save images manually (optional):
for i, content_block in enumerate(result["content"]):
    if "image" in content_block:
        image_bytes = content_block["image"]["source"]["bytes"]
        with open(f"spot_image_{i}.jpg", "wb") as f:
            f.write(image_bytes)
        print(f"Saved spot_image_{i}.jpg")
```

### Natural Language Control

```python
from strands import Agent
from strands_spot import use_spot

agent = Agent(tools=[use_spot])

# Agent interprets and executes
agent("""
Connect to Spot robot at 192.168.80.3 with admin credentials.
First, check the robot's battery level.
If battery is above 20%, make the robot stand up and wave.
Then capture images from all cameras and sit back down.
""")

# The agent will break this into atomic use_spot calls:
# 1. use_spot(service="robot_state", method="get_robot_state", ...)
# 2. use_spot(service="robot_command", method="stand", ...)
# 3. use_spot(service="robot_command", method="arm_ready", ...)
# 4. use_spot(service="image", method="get_image_from_sources", ...)
# 5. use_spot(service="robot_command", method="sit", ...)
```

### Vision-Enabled Agent (LLM Can See!)

```python
from strands import Agent
from strands_spot import use_spot

agent = Agent(tools=[use_spot])

# The agent can capture AND analyze images
response = agent("""
Connect to Spot at 192.168.80.3.
Take a picture from the front-left camera and tell me:
1. What objects do you see?
2. Is the path ahead clear?
3. Are there any obstacles?
""")

# Behind the scenes:
# 1. Agent calls use_spot(service="image", method="get_image_from_sources")
# 2. Tool returns image in LLM-readable format
# 3. Agent's vision model analyzes the image
# 4. Agent provides natural language response with image analysis

print(response)
# Output: "I can see a hallway with clear flooring. There's a door on the left
#          and some office furniture on the right. The path ahead is clear with
#          no obstacles detected within 5 meters."
```

### Real-World Scenario: Autonomous Inspection

```python
agent = Agent(tools=[use_spot])

# Complex multi-step task with vision
agent("""
Using Spot robot at 192.168.80.3:

1. Stand up and check battery level
2. Walk forward 2 meters
3. Capture images from all 5 cameras
4. Analyze the images and report:
   - Any equipment damage visible
   - Temperature gauge readings (if visible)
   - Safety hazards
5. Walk back 2 meters
6. Sit down and power off

Report your findings in a structured format.
""")

# The agent autonomously:
# - Plans the sequence of SDK calls
# - Executes motion commands
# - Captures multiple camera views
# - Analyzes visual data with vision models
# - Generates comprehensive inspection report
```

## Safety

**Before operating:**
- Clear 3m around robot
- Keep E-stop accessible  
- Verify Spot firmware compatibility (SDK 5.0+)

**During operation:**
```python
# Check robot state before commands
state = use_spot(service="robot_state", method="get_robot_state")

# Use timeouts to prevent hanging
use_spot(service="power", method="power_on", params={"timeout_sec": 20})

# Emergency stop
use_spot(service="robot_command", method="velocity_command",
         params={"v_x": 0.0, "v_y": 0.0, "v_rot": 0.0})
```

## License

Apache-2.0

---

<div align="center">
  <a href="https://github.com/cagataycali/strands-spot">GitHub</a>
  ◆ <a href="https://dev.bostondynamics.com">Spot SDK Docs</a>
  ◆ <a href="https://strandsagents.com/">Strands Docs</a>
</div>
