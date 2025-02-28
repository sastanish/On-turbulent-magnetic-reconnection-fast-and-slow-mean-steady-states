cmake_minimum_required(VERSION 3.13)

project(trm LANGUAGES CXX)
find_package(bout++ REQUIRED)
add_executable(trm trm.cxx)
target_link_libraries(trm PRIVATE bout++::bout++)
