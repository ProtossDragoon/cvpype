cmake_minimum_required(VERSION 3.27)
project(
    CVPYPE
    VERSION 0.0.1
    DESCRIPTION "Computer Vision Pipeline with Python Frontend"
    HOMEPAGE_URL "https://github.com/ProtossDragoon/cvpype"
)

cmake_path(APPEND CREATE_DOCUMENT_CMAKE_PATH ${CMAKE_CURRENT_SOURCE_DIR} "cmake" "create_document.cmake")
cmake_path(APPEND TEST_PYTHON_CMAKE_PATH ${CMAKE_CURRENT_SOURCE_DIR} "cmake" "test_python.cmake")
include(${CREATE_DOCUMENT_CMAKE_PATH})
include(${TEST_PYTHON_CMAKE_PATH})
