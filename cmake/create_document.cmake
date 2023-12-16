find_package(Doxygen)

if(NOT DOXYGEN_FOUND)
    message(FATAL_ERROR "Doxygen is needed to build the documentation.")
else()
    cmake_path(APPEND DOXYFILE_PATH ${CMAKE_CURRENT_SOURCE_DIR} "docs" "Doxyfile")
    if(EXISTS ${DOXYFILE_PATH})
        cmake_path(APPEND DOXYDOC_PATH ${CMAKE_CURRENT_SOURCE_DIR} "docs")
        message(STATUS ${DOXYFILE_PATH})
        add_custom_target(docs)
        add_custom_command(TARGET docs POST_BUILD
            COMMAND doxygen
            WORKING_DIRECTORY ${DOXYDOC_PATH}
            COMMENT "Generating documents ...")
        message(STATUS "Added generating the documentation with Doxygen. Generate documentation with `make docs` command.")
    else()
        message(WARNING "File not found: ${DOXYFILE_PATH}")
    endif()
endif()
