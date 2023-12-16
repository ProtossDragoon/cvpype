cmake_path(APPEND PYTHON_SRC_ROOT_DIR ${CMAKE_CURRENT_SOURCE_DIR} "cvpype" "python")
cmake_path(APPEND PYTHON_INTEGRATION_TEST_DIR ${CMAKE_CURRENT_SOURCE_DIR} "cvpype" "python" "tests" "integration")

add_custom_target(test)

if(EXISTS ${PYTHON_SRC_ROOT_DIR})
    add_custom_command(TARGET test POST_BUILD
        COMMAND python3 -m unittest discover -s ${PYTHON_SRC_ROOT_DIR}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        COMMENT "Run python unit tests ... ")
    message(STATUS "Added python unit test. Run unit tests with `make test` command.")
else()
    message(WARNING "Directory not found: ${PYTHON_SRC_ROOT_DIR}")
endif()

if(EXISTS ${PYTHON_INTEGRATION_TEST_DIR})
    add_custom_command(TARGET test POST_BUILD
        COMMAND python3 -m unittest discover -s ${PYTHON_INTEGRATION_TEST_DIR}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        COMMENT "Run python integration tests ... ")
    message(STATUS "Added python integration test. Run integration tests with `make test` command.")
else()
    message(WARNING "Directory not found: ${PYTHON_INTEGRATION_TEST_DIR}")
endif()
