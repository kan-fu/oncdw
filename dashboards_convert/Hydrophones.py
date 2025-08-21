import json
import re

import lxml.html
from onc import ONC
from util import extract_data_preview_option, extract_node_id_category_id

with open("./dashboards_convert/html/Hydrophones.html") as f:
    tree = lxml.html.fromstring(f.read())


res = []
for section in tree.xpath("//section[@class='oncWidgetGroup' and @id]/.."):
    # Get data preview options, format is [(data_product_format_id, plot_number), ...]
    data_preview_options = [
        extract_data_preview_option(ele.attrib["url"])
        for ele in section.xpath("./figure")
    ]

    # Get device name and device id, example is "50440Ocean Sonics icListen HF Hydrophone 6094"

    device_id, device_name = re.match(
        r"(\d+)(.*)", section.xpath(".//div[@class='device']")[0].text_content()
    ).groups()

    # Get location code and location name, example is "BFBR - FORCE Underwater Network - Black Rock"
    location_code, location_name = re.match(
        r"(.*) - (.*)\. Depth.* ", section.xpath("./h2")[0].text_content()
    ).groups()

    # Get node id and device category id
    node_id, device_category_id = extract_node_id_category_id(
        section.xpath("./figure[1]")[0].attrib["url"]
    )

    # Get device code and file extensions for archive file table
    device_code = section.xpath(".//section[@devicecode]")[0].attrib["devicecode"]
    file_extensions = (
        section.xpath(".//section[@extension]")[0]
        .attrib.get("extension", "")
        .split(", ")
    )

    onc = ONC("YOUR_TOKEN")

    location_info = onc.getLocations({"locationCode": location_code})

    res.append(
        {
            "device_name": device_name,
            "device_id": device_id,
            "location_code": location_code,
            "location_name": location_name,
            "search_tree_node_id": node_id,
            "device_category_id": device_category_id,
            "device_code": device_code,
            "data_preview_options": data_preview_options,
            "file_extensions": file_extensions,
            "lat": location_info[0]["lat"],
            "lon": location_info[0]["lon"],
        }
    )
with open("./pages/Hydrophones_Devices.json", "w") as f:
    json.dump(res, f, indent=2)
