FROM ros:humble

RUN apt-get update && apt-get install -y \
    python3-pip \
    ros-humble-nav2-msgs \
    ros-humble-geometry-msgs \
    ros-humble-sensor-msgs \
    ros-humble-tf2-ros \
    ros-humble-nav-msgs \
    ros-humble-std-msgs \
    ros-humble-rviz2

WORKDIR /workspace

CMD ["bash"]