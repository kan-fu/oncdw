from template import template2

json_filename = "Saanich_Inlet_BPS"
page_title = "Saanich Inlet BPS"

# For the links on the top

device = "Oceanworks Enclosure 001 (23129)"
device_console_url = "https://data.oceannetworks.ca/DC?TREETYPE=10&OBSERVATORY=8&STATION=100&DEVICE=1&DEVICE=23129&TAB=Device%20Control"
annotation_url_1 = "https://data.oceannetworks.ca/AnnotationsV2?dateFilter.fromDate&dateFilter.toDate&sourceFilter=3&sourceFilter=5&resourceFilter.resourceTypeId=1000&resourceFilter.resource.id=1210&resourceFilter.resource.name=S30006%20%281210%29&resourceFilter.includeTopology=true"
annotation_url_2 = "https://data.oceannetworks.ca/AnnotationsV2?dateFilter.fromDate&dateFilter.toDate&sourceFilter=3&sourceFilter=5&resourceFilter.resourceTypeId=1000&resourceFilter.resource.id=23129&resourceFilter.resource.name=Oceanworks%20Enclosure%20001%20%2823129%29&resourceFilter.includeTopology=true"
plotting_utility_url = (
    "https://data.oceannetworks.ca/PlottingUtility?refLink=MjI0NDZ8OTkzNw=HEQ"
)

links = {
    f"Oceans 3.0 Device Console - {device}": device_console_url,
    "Oceans 3.0 Annotation - Saanich Inlet Root Node (includes SI VIP)": annotation_url_1,
    "Oceans 3.0 Annotation - Saanich Inlet BPS": annotation_url_2,
    "Plotting Utility - SI BPS Profiler": plotting_utility_url,
}


template2(json_filename, page_title, links)
