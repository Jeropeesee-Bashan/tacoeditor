cmake_minimum_required(VERSION 3.10 FATAL_ERROR)
project(gl_preview C)

set(CMAKE_C_STANDARD 90)
set(CMAKE_C_EXTENSIONS ON)
set(CMAKE_C_STANDARD_REQUIRED ON)

find_package(PkgConfig REQUIRED)
pkg_check_modules(GTK4 REQUIRED gtk4)
pkg_check_modules(EPOXY REQUIRED epoxy)

set(SOURCES
    ${CMAKE_SOURCE_DIR}/gl_preview.c
    ${CMAKE_SOURCE_DIR}/gl_preview.h
)
set(GIR_OUTPUT ${CMAKE_BINARY_DIR}/Taco-1.0.gir)
set(TYPELIB_OUTPUT ${CMAKE_BINARY_DIR}/Taco-1.0.typelib)

add_library(taco_gl_preview SHARED ${SOURCES})

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

set(GIR_INCLUDE_DIRS ${GTK4_INCLUDE_DIRS})
list(TRANSFORM GIR_INCLUDE_DIRS PREPEND "-I")

add_custom_command(
    OUTPUT ${GIR_OUTPUT}
    COMMAND g-ir-scanner
    ARGS --warn-all
    --warn-error
    --namespace Taco
    --nsversion 1.0
    --library=taco_gl_preview
    --library-path=${CMAKE_BINARY_DIR}
    --include=Gtk-4.0
    --output ${GIR_OUTPUT}
    ${GIR_INCLUDE_DIRS}
    ${SOURCES}
    DEPENDS taco_gl_preview
)

add_custom_command(
    OUTPUT ${TYPELIB_OUTPUT}
    COMMAND g-ir-compiler ${GIR_OUTPUT} --output ${TYPELIB_OUTPUT}
    DEPENDS ${GIR_OUTPUT}
)

add_custom_target(generate-introspection ALL DEPENDS ${TYPELIB_OUTPUT})

install(TARGETS taco_gl_preview LIBRARY
    DESTINATION .
)

install(FILES ${TYPELIB_OUTPUT}
    DESTINATION girepository-1.0
)
