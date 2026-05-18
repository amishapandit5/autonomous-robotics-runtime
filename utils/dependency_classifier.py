ROS_DEPENDENCIES = [

    "rclpy",

    "nav2_msgs",

    "geometry_msgs",

    "sensor_msgs",

    "tf2_ros",

    "nav_msgs",

    "std_msgs",

    "visualization_msgs",

    "builtin_interfaces",

    "trajectory_msgs",

    "action_msgs",

    "cv_bridge",

    "tf_transformations",

    "ament_index_python"
]


BUILT_IN_MODULES = [

    "os",
    "sys",
    "math",
    "json",
    "time",
    "random",
    "subprocess",
    "threading",
    "asyncio",
    "pathlib",
    "datetime",
    "typing",
    "collections",
    "itertools",
    "functools",
    "statistics",
    "logging"
]


COMMON_PIP_PACKAGES = [

    "numpy",
    "opencv_python",
    "pandas",
    "matplotlib",
    "scipy",
    "requests",
    "yaml"
]


def classify_dependency(module_name):

    cleaned_module = (
        module_name
        .strip()
        .lower()
    )

    # BUILT-IN
    if cleaned_module in [

        module.lower()

        for module in BUILT_IN_MODULES
    ]:

        return "built_in"

    # ROS
    if cleaned_module in [

        module.lower()

        for module in ROS_DEPENDENCIES
    ]:

        return "ros"

    # COMMON PIP
    if cleaned_module in [

        module.lower()

        for module in COMMON_PIP_PACKAGES
    ]:

        return "pip"

    # UNKNOWN MODULES
    return "unknown"