cmake_minimum_required(VERSION 3.12)
project(engine)
set(CMAKE_CXX_STANDARD 17)

add_library(Engine_executable SHARED
        src/board.cpp
        src/figure.cpp
        src/main.h
        ../dependencies/nlohmann/json/json-master/single_include/nlohmann/json.hpp)

