from template import Barkley

json_filename = "Cascadia_Devices"
location_code = "NC27"
page_title = "Cascadia Basin"

# For the links on the top
device_name_id = "OceanWorks Junction Box JB-01 (10515)"
device_console_url = "https://data.oceannetworks.ca/DC?TREETYPE=10&OBSERVATORY=8&STATION=102&DEVICE=10501&DEVICE=10515&TAB=Device%20Control"
annotation_url = "https://data.oceannetworks.ca/AnnotationsV2?sourceFilter=3&sourceFilter=5&resourceFilter.resourceTypeId=1000&resourceFilter.resource.id=10515&resourceFilter.resource.name=OceanWorks%20Junction%20Box%20JB-01%20%2810515%29&resourceFilter.includeTopology=true&fieldFilter"

Barkley(
    json_filename,
    location_code,
    page_title,
    device_name_id,
    device_console_url,
    annotation_url,
)
