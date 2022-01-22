--This tries to activate a conda env without using "source activate"


-- The base path to the conda environment
--local root = "/home/darstr1/miniconda3-module"
local root = "/shared/software/anaconda3"
local name = "blah"


-- Descriptions and help
whatis("Loads the conda envirnment $root")

-- only one conda module can be loaded at once:
family("conda")

-- Core module definitions
local condadir, condaname = splitFileName(root)
local name = name or condaname

prepend_path("PATH", pathJoin(root, "bin"))
pushenv("CONDA_PREFIX", root)
pushenv("CONDA_PROMPT_MODIFIER", table.concat({"(", name, ") "}))
pushenv("CONDA_EXE", pathJoin(root, "bin/conda"))
pushenv("CONDA_PYTHON_EXE", pathJoin(root, "bin/python"))
--CONDA_SHLVL=1
--CONDA_DEFAULT_ENV=base


-- Source the conda.sh initialization script.
local moddir, modfile = splitFileName(myFileName())

execute{cmd=table.concat({"source ", pathJoin(moddir, "conda.sh")}),
        modeA={"unload"}}

execute{cmd="unset conda", modeA={"unload"}}
