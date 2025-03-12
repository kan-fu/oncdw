from template import Barkley

json_filename = "Barkley_Upper_Slope_Devices"
location_code = "NCBC"
page_title = "Barkley Upper Slope"

# For the links on the top
device_name_id = "OceanWorks Junction Box JB-06 (10003)"
device_console_url = "https://data.oceannetworks.ca/DC?TREETYPE=10&OBSERVATORY=8&STATION=102&DEVICE=10001&DEVICE=10003&TAB=Device%20Control"
annotation_url = "https://data.oceannetworks.ca/AnnotationsV2?sourceFilter=3&sourceFilter=5&resourceFilter.resourceTypeId=1000&resourceFilter.resource.id=10003&resourceFilter.resource.name=OceanWorks%20Junction%20Box%20JB-06%20%2810003%29&resourceFilter.includeTopology=true"

Barkley(
    json_filename,
    location_code,
    page_title,
    device_name_id,
    device_console_url,
    annotation_url,
)
