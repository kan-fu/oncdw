from util import template_ferry_gen

html_filename = "ferry_sovi"
json_filename = "Ferry_SoVI"

# Change "<a href="#wf_20"><span class="device"><span>29</span>AandOpt0418 in TWSB </span></a>"
# to "<a href="#wf_20"><span class="device"><span>23203</span>AandOpt1797 in TWSB </span></a>" at line 56
template_ferry_gen(html_filename, json_filename)
