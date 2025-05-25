cmake_minimum_required(VERSION 3.10 FATAL_ERROR)
project(tacoeditor C)

set(CMAKE_C_STANDARD 90)
set(CMAKE_C_EXTENSIONS ON)
set(CMAKE_C_STANDARD_REQUIRED ON)

if(CMAKE_C_COMPILER_ID STREQUAL "Clang")
    set(CMAKE_C_STANDARD 11)
endif()

find_package(PkgConfig REQUIRED)
pkg_check_modules(GTK4 REQUIRED gtk4)
pkg_check_modules(EPOXY REQUIRED epoxy)

set(SOURCES
    ${CMAKE_SOURCE_DIR}/gl_preview.c
    ${CMAKE_SOURCE_DIR}/gl_preview.h
)

add_library(tacoeditor SHARED ${SOURCES})

target_include_directories(tacoeditor PRIVATE
    ${GTK4_INCLUDE_DIRS}
    ${EPOXY_INCLUDE_DIRS}
)

target_link_libraries(tacoeditor PRIVATE
    ${GTK4_LIBRARIES}
    ${EPOXY_LIBRARIES}
)

if(MSVC)
    check_c_compiler_flag("/Zc:gnu" HAS_GNU_EXTENSIONS)
    if(HAS_GNU_EXTENSIONS)
        target_compile_options(tacoeditor PRIVATE /Zc:gnu)
    endif()
    target_compile_options(tacoeditor PRIVATE /W4 /WX)
else()
    target_compile_options(tacoeditor PRIVATE -Wall -Wextra -Werror)
endif()

set(GIR_OUTPUT ${CMAKE_BINARY_DIR}/TacoEditor-1.0.gir)
set(TYPELIB_OUTPUT ${CMAKE_BINARY_DIR}/TacoEditor-1.0.typelib)
set(GIR_INCLUDE_DIRS ${GTK4_INCLUDE_DIRS})
list(TRANSFORM GIR_INCLUDE_DIRS PREPEND "-I")

add_custom_command(
    OUTPUT ${GIR_OUTPUT}
    COMMAND g-ir-scanner
    ARGS --warn-all
    --warn-error
    --namespace=TacoEditor
    --nsversion=1.0
    --library=tacoeditor
    --library-path=${CMAKE_BINARY_DIR}
    --include=Gtk-4.0
    --output=${GIR_OUTPUT}
    ${GIR_INCLUDE_DIRS}
    ${SOURCES}
    DEPENDS tacoeditor
)

add_custom_command(
    OUTPUT ${TYPELIB_OUTPUT}
    COMMAND g-ir-compiler
    ARGS --output=${TYPELIB_OUTPUT}
    --shared-library=$<TARGET_FILE_NAME:tacoeditor>
    ${GIR_OUTPUT}
    DEPENDS ${GIR_OUTPUT}
)

add_custom_target(typelib ALL DEPENDS ${TYPELIB_OUTPUT})

install(TARGETS tacoeditor DESTINATION .)
install(FILES ${TYPELIB_OUTPUT} DESTINATION .)
