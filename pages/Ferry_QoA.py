from template import template2

json_filename = "Ferry_QoA"
page_title = "QoA Tsawwassen - Duke Point"

# For the links on the top
device = "Queen of Alberni (22910)"
device_console_url = "https://data.oceannetworks.ca/DC?TREETYPE=10&OBSERVATORY=8&STATION=205&DEVICE=22910&TAB=Device%20Control"
annotation_url = "https://data.oceannetworks.ca/AnnotationsV2?sourceFilter=3&sourceFilter=5&resourceFilter.resourceTypeId=1000&resourceFilter.resource.id=22910&resourceFilter.resource.name=Queen%20of%20Alberni%20%2822910%29&resourceFilter.includeTopology=true"
marine_traffic_url = "https://www.marinetraffic.com/en/ais/details/ships/shipid:379852/mmsi:316001245/imo:7414080/vessel:QUEEN_OF_ALBERNI"
plotting_utility_url = (
    "https://data.oceannetworks.ca/PlottingUtility?refLink=MjI0NDZ8OTkyMw=HEQ"
)

links = {
    f"Oceans 3.0 Device Console - {device}": device_console_url,
    f"Oceans 3.0 Annotation - {device}": annotation_url,
    f"Marine Traffic - {device}": marine_traffic_url,
    f"Plotting Utility - {device}": plotting_utility_url,
}


template2(json_filename, page_title, links)
