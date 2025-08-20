import json

import lxml.html
from onc import ONC
from util import extract_data_preview_option, extract_node_id_category_id

with open("./dashboards_convert/html/AcousticDevices.html") as f:
    tree = lxml.html.fromstring(f.read())


res = []
for section in tree.xpath("//section[@class='oncWidgetGroup' and @id]"):
    # Get data preview options, format is [(data_product_format_id, plot_number), ...]
    data_preview_options = [
        extract_data_preview_option(ele.attrib["url"])
        for ele in section.xpath("./figure")
    ]

    # Get device name and device id, example is "Nortek AWAC AST 400 kHz 2226 - 22956"
    device_name, device_id = (
        section.xpath("./h3")[0].text_content().rsplit(" - ", maxsplit=1)
    )

    # Get location code and location name, example is "BFBR - FORCE Underwater Network - Black Rock"
    location_code, location_name = (
        section.xpath("./h2")[0].text_content().split(" - ", maxsplit=1)
    )

    # Get node id and device category id
    node_id, device_category_id = extract_node_id_category_id(
        section.xpath("./figure[1]")[0].attrib["url"]
    )

    # Get device code
    device_code = section.xpath(".//section[@devicecode]")[0].attrib["devicecode"]

    onc = ONC("TOKEN")

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
            "lat": location_info[0]["lat"],
            "lon": location_info[0]["lon"],
        }
    )
with open("./pages/Acoustic_Devices.json", "w") as f:
    json.dump(res, f, indent=2)
