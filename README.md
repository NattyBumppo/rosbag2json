# rosbag2json
A converter that takes ROS bag files and turns them into JSON files. This code was inspired by/derived from Nick Speal's **bag2csv** project, in his [ROStools](https://github.com/nickspeal/ROStools) repository.

Notes:

- JSON files are text, and they're big! Giant bags will become giant-er JSONs, as far as file size is concerned.
- This code has some dependencies related to ROS that you'll need in order to get it working. Minimally, you should be able to get it working if you install [catkin](https://github.com/ros/catkin), [rosgraph](https://github.com/ros/ros_comm/tree/kinetic-devel/tools/rosgraph), [roslib](https://github.com/ros/ros/tree/kinetic-devel/core/roslib), and [rospy](https://github.com/ros/ros_comm/tree/kinetic-devel/clients/rospy). (I struggled with dependency hell for over an hour to figure this out; now that you know this, hopefully you won't have to.)
- Performance for certain types of pathological messages (e.g., extremely long lists of objects with several properties each) is quite slow due to the recursive code used to build the hierarchies. This could probably be optimized; I might do so at a later date.