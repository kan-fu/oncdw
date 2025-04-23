from template import Barkley

json_filename = "China_Creek_Devices"
location_code = "CCIP"
page_title = "China Creek"

# For the links on the top
device_name_id = "China Creek Drivers (44000)"
device_console_url = "https://data.oceannetworks.ca/DC?TREETYPE=10&OBSERVATORY=8&STATION=175&DEVICE=44000&TAB=Device%20Control"
annotation_url = "https://data.oceannetworks.ca/AnnotationsV2?sourceFilter=3&sourceFilter=5&resourceFilter.resourceTypeId=1000&resourceFilter.resource.id=44000&resourceFilter.resource.name=China%20Creek%20Drivers%20%2844000%29&resourceFilter.includeTopology=true"


Barkley(
    json_filename,
    location_code,
    page_title,
    device_name_id,
    device_console_url,
    annotation_url,
)
