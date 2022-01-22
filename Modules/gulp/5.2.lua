--# Local variables
--a) Version is equal to file name (for more intrinsic functions see /opt/Lmod/lmod/6.0.1/libexec/modfuncs.lua)
--this program compiled by intel compiler
local ver      = myModuleVersion()

--b) base_dir, wiki, support
local base_dir = pathJoin("/shared/software/chem/gulp",ver)
local wiki     = "http://gulp.curtin.edu.au/gulp/"

local compiler = 'intel'

local mpi = 'impi'


--# Whatis description
whatis("GULP (Version ",ver,") is a package for displaying Molecular Densities and Molecular Coordinates (command: 'gulp')")

--# Environment Variables
setenv("GULP_VERSION", ver)
setenv("GULP_BIN_DIR", pathJoin(base_dir, "Src"))
setenv("GULP_LIB", pathJoin(base_dir, "Libraries "))
setenv("GULP_DOC", pathJoin(base_dir, "Docs"))

--# PATH, MANPATH, LD_LIBRARY_PATH etc.
prepend_path("PATH",    pathJoin(base_dir, "Src"))

-- load the default impi module for MPI launcher

load('intel')
load('impi')


--# Help description
help([[
This module provides the package GULP version 5.2 via commands:
  'gulp < <coordinate_file.gin>'

Documentation:
* Developer website: http://gulp.curtin.edu.au/gulp/
Module is written by Mersad Mostaghimi <mersad.mostaghimi@kit.edu>
]])

--# Set family (= generalized prereq/conflict function) for this module
--family("gulp")

--# Set conflict
conflict("gulp")
