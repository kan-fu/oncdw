import json

import lxml.html
from util import extract_dp_format_id_plot_number, extract_node_id_category_id

with open("./dashboards_convert/html/AcousticDevices.html") as f:
    tree = lxml.html.fromstring(f.read())


res = []
for section in tree.xpath("//section[@class='oncWidgetGroup' and @id]"):
    # Get data preview options, format is [(data_product_format_id, plot_number), ...]
    data_preview_options = [
        extract_dp_format_id_plot_number(ele.attrib["url"])
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

    res.append(
        {
            "deviceName": device_name,
            "deviceId": device_id,
            "locationCode": location_code,
            "locationName": location_name,
            "searchTreeNodeId": node_id,
            "deviceCategoryId": device_category_id,
            "deviceCode": device_code,
            "dataPreviewOptions": data_preview_options,
        }
    )
with open("./pages/Acoustic_Devices.json", "w") as f:
    json.dump(res, f, indent=2)
