#!/bin/bash
. /etc/profile.d/lmod.sh
set -e
module purge
module load vasp prun
{% if WaNo["TABS"]["Files_Run"]["SOC"] -%}
{{ "prun vasp_ncl"  }}
{% else %}
{{ "prun" }} {{ WaNo["TABS"]["Files_Run"]["prun_vasp"] }}
{%- endif %}
