cmake_minimum_required(VERSION 3.10 FATAL_ERROR)
project(gl_preview C)

set(CMAKE_C_STANDARD 90)
set(CMAKE_C_EXTENSIONS ON)
set(CMAKE_C_STANDARD_REQUIRED ON)

find_package(PkgConfig REQUIRED)
pkg_check_modules(GTK4 REQUIRED gtk4)
pkg_check_modules(EPOXY REQUIRED epoxy)

add_library(taco_gl_preview SHARED
    gl_preview.c
)

target_include_directories(taco_gl_preview PRIVATE
    ${GTK4_INCLUDE_DIRS}
    ${EPOXY_INCLUDE_DIRS}
)

target_link_libraries(taco_gl_preview PRIVATE
    ${GTK4_LIBRARIES}
    ${EPOXY_LIBRARIES}
)

if(MSVC)
    check_c_compiler_flag("/Zc:gnu" HAS_GNU_EXTENSIONS)
    if(HAS_GNU_EXTENSIONS)
        target_compile_options(taco_gl_preview PRIVATE /Zc:gnu)
    endif()
    target_compile_options(taco_gl_preview PRIVATE /W4 /WX)
else()
    target_compile_options(taco_gl_preview PRIVATE -Wall -Wextra -Werror)
endif()

install(TARGETS taco_gl_preview
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
)
