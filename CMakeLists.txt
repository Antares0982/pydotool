cmake_minimum_required(VERSION 3.18)
# find correct python package is implemented in cmake 3.15, find other implementation is in 3.18

project(ydotool C)

set(CMAKE_C_STANDARD 99)

find_package(Python3 COMPONENTS Development)
# Include GNU install directory module to detect where to install
# files on Linux/Unix systems (e.g., lib vs lib64)
include(GNUInstallDirs)
find_package(PkgConfig)


execute_process(COMMAND git describe --tags --long --always RESULT_VARIABLE RC_GIT_VER OUTPUT_VARIABLE GIT_VERSION)

if (${RC_GIT_VER} EQUAL 0)
    string(STRIP ${GIT_VERSION} GIT_VERSION)
    message("-- Version: " ${GIT_VERSION})
    add_definitions(-DVERSION=\"${GIT_VERSION}\")
endif()

set(SOURCE_FILES_CLIENT ydotool/ydotool.c ydotool/pydotool.c)

add_library(_pydotool SHARED ${SOURCE_FILES_CLIENT})
target_include_directories(_pydotool PRIVATE ${Python3_INCLUDE_DIRS} ydotool)
target_link_libraries(_pydotool ${Python3_LIBRARIES})

if (CMAKE_C_COMPILER_ID STREQUAL "GNU" OR CMAKE_C_COMPILER_ID STREQUAL "Clang")
    target_compile_options(_pydotool PUBLIC -Wno-unused-result)
endif()

# optimize for Release build
if (CMAKE_BUILD_TYPE MATCHES ".*Rel.*")
    message("Release mode, enabling maximal optimization")
    target_compile_options(_pydotool PUBLIC -O3)
else(CMAKE_BUILD_TYPE MATCHES ".*Rel.*")
    message("Debug mode, enabling debug symbols")
    target_compile_options(_pydotool PUBLIC -g)
endif (CMAKE_BUILD_TYPE MATCHES ".*Rel.*")

# install py package
install(TARGETS _pydotool LIBRARY DESTINATION .)
set_target_properties(_pydotool PROPERTIES PREFIX "")
