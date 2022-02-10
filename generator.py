# Copyright (c) 2018-2020, Jason DeGraw
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
import os

toplevel_cmakelists_txt = {
    'vanilla' : '''
project(%s)

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

add_subdirectory(src)
''',
    'c++11' : '''
cmake_minimum_required(VERSION 2.8.11)

project(%s)

if(CMAKE_COMPILER_IS_GNUCXX)
  # 4.6 is the earliest version supporting nullptr and range-based for
  # https://gcc.gnu.org/projects/cxx0x.html
  if(${CMAKE_CXX_COMPILER_VERSION} VERSION_LESS "4.6.0")
    message(FATAL_ERROR "g++ versions earlier than 4.6.0 are not supported")
  endif()
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
elseif(MSVC)
  # http://en.wikipedia.org/wiki/Visual_C%%2B%%2B#32-bit_and_64-bit_versions
  if(${CMAKE_C_COMPILER_VERSION} VERSION_LESS "18.0.21005.1")
    message(FATAL_ERROR "Visual Studio earlier than VS2013 is not supported")
  endif()
elseif("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
  # Need to check for clang version
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -stdlib=libc++")
endif()

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

add_subdirectory(src)
''',
    'c++17' : '''
cmake_minimum_required(VERSION 2.8.11)

project(%s)

if(CMAKE_COMPILER_IS_GNUCXX)
  # 4.6 is the earliest version supporting nullptr and range-based for
  # https://gcc.gnu.org/projects/cxx-status.html
  if(${CMAKE_CXX_COMPILER_VERSION} VERSION_LESS "7.0.0")
    message(FATAL_ERROR "g++ versions earlier than 7.0.0 are not supported")
  endif()
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17")
elseif(MSVC)
  # http://en.wikipedia.org/wiki/Visual_C%%2B%%2B#32-bit_and_64-bit_versions
  if(${CMAKE_C_COMPILER_VERSION} VERSION_LESS "19.10.25017.0")
    message(FATAL_ERROR "Visual Studio earlier than VS2019 is not supported")
  endif()
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /std:c++latest")
elseif("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
  # Need to check for clang version
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -stdlib=libc++")
endif()

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

add_subdirectory(src)
''',
    'c++20' : '''
cmake_minimum_required(VERSION 2.8.11)

project(%s)

if(CMAKE_COMPILER_IS_GNUCXX)
  # C++ 20 is allegedly available beginning in GCC v8
  # https://gcc.gnu.org/projects/cxx-status.html#cxx20
  if(${CMAKE_CXX_COMPILER_VERSION} VERSION_LESS "8.0.0")
    message(FATAL_ERROR "g++ versions earlier than 8.0.0 are not supported")
  endif()
  if(${CMAKE_CXX_COMPILER_VERSION} VERSION_LESS "10.0.0")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++2a")
  else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++20")
  endif()
elseif(MSVC)
  # https://devblogs.microsoft.com/cppblog/msvc-cpp20-and-the-std-cpp20-switch/
  if(${CMAKE_C_COMPILER_VERSION} VERSION_LESS "19.29.30040.0")
    message(FATAL_ERROR "Visual Studio earlier than VS2019 16.11 is not supported")
  endif()
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /std:c++20")
elseif("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
  # Need to check for clang version
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++20 -stdlib=libc++")
endif()

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

add_subdirectory(src)
'''}

srcdir_cmakelists_txt = {
    'vanilla' : '''
project(%s)

add_executable(%s %s.cpp)
'''}

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='.')
    #parser.add_argument('project', metavar='PROJECT')
    #parser.add_argument('-o', '--output', dest='outpath', action='store',
    #                    default='.',
    #                    help='path to generate output in')
    parser.add_argument('-s', '--standard', dest='standard', action='store',
                        default='vanilla',
                        help='C++ standard to use')
    parser.add_argument('-p', '--project', dest='project', action='store',
                        default='project',
                        help='specify project name')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='operate verbosely')
    parser.add_argument('--list-standards', dest='list_and_exit', action='store_true',
                        help='list the allegedly supported standards and exit')

    args = parser.parse_args()

    if args.list_and_exit:
        for k,v in toplevel_cmakelists_txt.items():
            print(k)
        exit()

    if not args.standard in toplevel_cmakelists_txt:
        args.standard = 'vanilla'

    txt = toplevel_cmakelists_txt[args.standard] % args.project

    fp = open('CMakeLists.txt', 'w')
    fp.write(txt)
    fp.close()

    os.mkdir('src')
    os.chdir('src')

    txt = srcdir_cmakelists_txt['vanilla'] % (args.project,
                                              args.project,
                                              args.project)

    fp = open('CMakeLists.txt', 'w')
    fp.write(txt)
    fp.close()

    fp = open('%s.cpp' % args.project, 'w')
    fp.close()

