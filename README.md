# ROS Telepresence Service Robot

Archived ROS-based service robot prototype with web video streaming, remote browser control, audio streaming, ROS bridge support, serial communication, and thermal camera launch files.

The project was originally built during the COVID-era service robot period. It is kept as a reference for the robot control architecture and integration experiments rather than as production-ready robotics software.

![Service robot prototype](https://user-images.githubusercontent.com/41507280/111017948-4309ba00-83f1-11eb-9d40-ea82d2199291.jpg)

## Features

- Tkinter launcher for starting and stopping robot services
- ROS web video streaming through `web_video_server`
- Astra camera and USB thermal camera launch commands
- ROS bridge websocket startup
- ROS serial startup for microcontroller communication
- Browser-based teleoperation UI
- Simple socket-based audio client/server prototype
- Separate Windows and Ubuntu experiment folders

## Repository Layout

- `main.py` - Legacy Python 2 Tkinter launcher for ROS services.
- `Ubuntu/` - Python 3 Flask/video-streaming experiment files.
- `Windows/` - Windows-oriented copy of the Flask/video-streaming experiment files.
- `html/` - Browser UI for robot video and teleoperation.
- `ros_bridge/` - ROS package with bridge/listener/talker scripts.
- `usb_cam-develop/` - Vendored ROS USB camera package used for thermal camera launch experiments.
- `web_video_server/` and `async_web_server_cpp/` - Vendored ROS web video dependencies.

## Requirements

- ROS Kinetic-era environment
- Python 2 for the legacy root `main.py`
- Python 3 for the `Ubuntu/` and `Windows/` Flask experiments
- Astra camera ROS package
- `rosbridge_server`
- `rosserial_python`
- `web_video_server`
- USB camera support
- Python packages listed in `requirements.txt`

Install Python packages for the Flask/audio/video experiments:

```bash
pip install -r requirements.txt
```

## Configuration

The launcher reads `config.json`:

```json
{
  "robotIp": "192.168.1.10"
}
```

Update `robotIp` to match the robot or remote computer on your network.

## Legacy Launcher

From a ROS environment:

```bash
python2 main.py
```

The launcher starts these commands:

```text
rosrun web_video_server web_video_server
roslaunch astra_camera astra.launch
roslaunch rosbridge_server rosbridge_websocket.launch
rosrun rosserial_python serial_node.py /dev/ttyACM0
roslaunch usb_cam thermal_cam.launch
python server.py
python client.py <robot-ip>
```

## Notes

- This repository is archived and kept for historical/reference value.
- Several ROS packages are vendored directly in the repository. For a production project, use proper ROS package dependencies or submodules instead.
- The code targets an older ROS/Python environment and may need updates for modern ROS Noetic/ROS 2 setups.
- No real network credentials are stored in this repository.

## Author

Alireza Ahmadi
