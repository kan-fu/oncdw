from util import template_gen

location_code = "CCIP"
location_name = "China Creek Underwater Network"
html_filename = "ChinaCreek_devices"
json_filename = "China_Creek_Devices"

# No device code for the archive file section. Need to add it manually for device 74100.
template_gen(location_code, location_name, html_filename, json_filename)
