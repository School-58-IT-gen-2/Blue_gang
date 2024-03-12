cmake_minimum_required(VERSION 3.12)
project(chess)
set(CMAKE_CXX_STANDARD 17)

add_subdirectory(engine)
add_executable(Main_executable main.cpp)

target_link_libraries(Main_executable Engine_executable)

message("C Compiler: ${CMAKE_C_COMPILER}")
message("C++ Compiler: ${CMAKE_CXX_COMPILER}")


add_custom_command(TARGET Main_executable POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
        ${CMAKE_SOURCE_DIR}/default_positions.json $<TARGET_FILE_DIR:Main_executable>)