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
  # http://en.wikipedia.org/wiki/Visual_C%2B%2B#32-bit_and_64-bit_versions
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
    parser.add_argument('-o', '--output', dest='outfile', action='store',
                        default='std211.xml',
                        help='file to save BSXML output in')
    parser.add_argument('-p', '--project', dest='project', action='store',
                        default='project',
                        help='specify project name')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='operate verbosely')

    args = parser.parse_args()

    txt = toplevel_cmakelists_txt['vanilla'] % args.project

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

