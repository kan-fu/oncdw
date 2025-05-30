from template import Ferry

json_filename = "Ferry_SoVI"
page_title = "SoVI Tsawwassen - Swartz Bay"

# For the links on the top
device_name_id = "Queen of Alberni (22910)"
device_console_url = "https://data.oceannetworks.ca/DC?TREETYPE=10&OBSERVATORY=8&STATION=115&DEVICE=22911&TAB=Device%20Control"
annotation_url = "https://data.oceannetworks.ca/AnnotationsV2?sourceFilter=3&sourceFilter=5&resourceFilter.resourceTypeId=1000&resourceFilter.resource.id=22911&resourceFilter.resource.name=Spirit%20of%20Vancouver%20Island%20%2822911%29&resourceFilter.includeTopology=true"
marine_traffic_url = "https://www.marinetraffic.com/en/ais/details/ships/shipid:379873/mmsi:316001269/imo:9030682/vessel:SPIRIT_OF_VANCOUVER_ISLAND"
plotting_utility_url = (
    "https://data.oceannetworks.ca/PlottingUtility?refLink=MjI0NDZ8OTkyNA=HEQ"
)


Ferry(
    json_filename,
    page_title,
    device_name_id,
    device_console_url,
    annotation_url,
    marine_traffic_url,
    plotting_utility_url,
)
