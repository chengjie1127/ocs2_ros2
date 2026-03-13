cmake_minimum_required(VERSION 3.10)
project(ocs2_self_collision)

find_package(ament_cmake_ros REQUIRED)
find_package(Boost REQUIRED COMPONENTS system filesystem log_setup log)
find_package(ocs2_pinocchio_interface REQUIRED)
find_package(pinocchio REQUIRED)

find_library(TINYXML_LIBRARY NAMES tinyxml REQUIRED)
find_path(TINYXML_INCLUDE_DIR NAMES tinyxml.h REQUIRED)

add_library(${PROJECT_NAME} SHARED
  src/PinocchioGeometryInterface.cpp
  src/SelfCollisionConstraint.cpp
  src/SelfCollision.cpp
)

target_include_directories(${PROJECT_NAME} PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  ${TINYXML_INCLUDE_DIR}
)

# 直接链接库路径，不再使用 tinyxml2::tinyxml2 别名
target_link_libraries(${PROJECT_NAME} PUBLIC 
  ocs2_pinocchio_interface::ocs2_pinocchio_interface
  pinocchio::pinocchio
  ${TINYXML_LIBRARY}
  Boost::system
  Boost::filesystem
  Boost::log_setup
  Boost::log
)

ament_export_include_directories(include)
ament_export_libraries(${PROJECT_NAME})
ament_export_dependencies(ocs2_pinocchio_interface pinocchio)

# Install library
install(TARGETS ${PROJECT_NAME}
  EXPORT export_${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

# Install headers
install(DIRECTORY include/
  DESTINATION include
)

ament_package()
