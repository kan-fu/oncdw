from util import template_gen

location_code = "FGPD"
location_name = "Folger Deep"
html_filename = "FolgerDeep_devices"
json_filename = "Folger_Deep_Devices"

# Manually set device code of DI 23235 to ICLISTENHF1266
template_gen(location_code, location_name, html_filename, json_filename)
