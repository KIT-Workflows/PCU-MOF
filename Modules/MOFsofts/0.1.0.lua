-- A module to load the MOFsofts
-- Developed by: Mersad.Mostaghimi@kit.edu

local name = 'MOFsofts'
local version = '0.1.0'

local root = "/shared/software/chem/MOFsofts/"

load('anaconda3')

prepend_path('PATH', root .. '/bin')
prepend_path('PATH', root .. '/autografs')
setenv('AuToGraFS_HOME', root .. 'autografs')

whatis('Enable usage of ' .. name .. ' ' .. version)

help([[
This modulefile configures the runtime environment of MOFsofts

It consist of several software that is used by MOF workflows in simstack or by individual 

For using any of them have a look on their help by running the software name by -h option

List of software that is avalable:
lcmaker
mofgen

For support please contact Mersad Mostaghimi <mersad.mostaghimi@kit.edu>

]])

