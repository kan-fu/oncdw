import json
import re

import lxml.html


def extract_dp_format_id_plot_number(url: str) -> tuple[int, int, int]:
    """
    Extract data product format id and plot number (and optionally sensor code id if exists) from the url.

    Return the tuple of (data_product_format_id, plot_number, sensor_code_id).
    """

    dp_format_id, plot_number = re.search(
        r"dataProductFormatId=(\d+)&plotNumber=(\d+)", url
    ).groups()

    query = re.search(r"sensorCodeId=(\d+)", url)

    # Extract sensor code id if present
    sensor_code_id = query.group(1) if query else 0

    return (int(dp_format_id), int(plot_number), int(sensor_code_id))


def extract_node_id_category_id(url: str) -> tuple[int, int]:
    """
    SearchTreeNodeId and DeviceCategoryId belong to device, so most of time they should be called once
    even when there are multiple data preview plots for the same device.
    """
    return tuple(
        map(
            int,
            re.search(r"searchTreeNodeId=(\d+)&deviceCategoryId=(\d+)", url).groups(),
        )
    )


def template_gen(location_code, location_name, html_filename, json_filename):
    with open(f"./dashboards_convert/html/{html_filename}.html") as f:
        tree = lxml.html.fromstring(f.read())

    # Get device id - device code pair from sidebar
    tmp = []
    for ele in tree.xpath("//span[@class='device']"):
        device_id_code = ele.text_content()
        pair = re.match(r"(\d+)(.*) ", device_id_code)
        if pair:
            tmp.append(pair.groups())
    device_code = dict(tmp)

    # device -> time_series for each sensor
    res1 = []
    for h3 in tree.xpath("//h3[./following-sibling::section]"):
        # Example h3 text content is "BACAX. Depth: 983.0 m - Nortek Aquadopp HR-Profiler 2 MHz 2700 - 11302 Device Details"
        _, device_name, device_id = (
            h3.text_content().replace("  Device Details", "").split(" - ")
        )

        # Get sensors, format is [(sensor_id, sensor_name), ...]
        sensors = [
            re.match(r"(\d+)(.*)", ele.text_content()).groups()
            for ele in h3.getnext().xpath(".//div[@class='sensor']")
        ]

        res1.append(
            {
                "deviceId": device_id,
                "deviceName": device_name,
                "sensors": sensors,
                "locationCode": location_code,
                "locationName": location_name,
                "deviceCode": device_code[device_id],
            }
        )

    # Extract two sensors time series (from two devices)
    devices = [
        device
        for ele in tree.xpath("//div[@class='device']")
        if "&" in (device := ele.text_content())
    ]
    sensors = [
        sensor
        for ele in tree.xpath("//div[@class='sensor']")
        if "," in (sensor := ele.text_content())
    ]

    for device, sensor in zip(devices, sensors, strict=False):
        device_id, device_name = re.match(r"(\d+ & \d+)(.*)", device).groups()
        device_id1, device_id2 = device_id.split(" & ")
        sensor_id1, sensorid2, sensor_name = re.match(
            r"(\d+),(\d+)(.*)", sensor
        ).groups()
        res1.append(
            {
                "deviceId": device_id,
                "deviceName": device_name,
                "sensors": [((sensor_id1, sensor_name), (sensorid2, sensor_name))],
                "locationCode": location_code,
                "locationName": location_name,
                "deviceCode": f"{device_code[device_id1]} & {device_code[device_id2]}",
            }
        )

    # device -> data preview plots + archive file table
    res2 = []
    for h3 in tree.xpath("//h3[./following-sibling::figure]"):
        _, device_name, device_id = (
            h3.text_content().replace("  Device Details", "").split(" - ")
        )
        section_div = h3.getparent().getparent()

        # Get data preview options, format is [(data_product_format_id, plot_number), ...]
        data_preview_options = [
            extract_dp_format_id_plot_number(ele.attrib["url"])
            for ele in section_div.xpath(".//figure")
        ]

        # Get node id and device category id
        node_id, device_category_id = extract_node_id_category_id(
            section_div.xpath(".//figure[1]")[0].attrib["url"]
        )

        # Get device code and filter extension (if present) for archive file query
        try:
            archive_file_section = section_div.xpath(".//section[@devicecode]")[0]
            device_code = archive_file_section.attrib["devicecode"]

            file_extensions = archive_file_section.get("extension")
            if file_extensions:
                file_extensions = file_extensions.split(", ")
        except IndexError:
            print("No archive file section found")
            device_code = None
            file_extensions = None

        res2.append(
            {
                "deviceId": device_id,
                "deviceName": device_name,
                "locationCode": location_code,
                "locationName": location_name,
                "dataPreviewOptions": data_preview_options,
                "searchTreeNodeId": node_id,
                "deviceCategoryId": device_category_id,
                "deviceCode": device_code,
                "fileExtensions": file_extensions,
            }
        )

    with open(f"./pages/{json_filename}_1.json", "w") as f:
        json.dump(res1, f, indent=2)

    with open(f"./pages/{json_filename}_2.json", "w") as f:
        json.dump(res2, f, indent=2)


def template_ferry_gen(html_filename, json_filename):
    with open(f"./dashboards_convert/html/{html_filename}.html") as f:
        tree = lxml.html.fromstring(f.read())

    # Get device id - device code pair from sidebar
    tmp = []
    for ele in tree.xpath("//span[@class='device']"):
        device_id_code = ele.text_content()
        pair = re.match(r"(\d+)(.*) in.*", device_id_code)
        if pair:
            tmp.append(pair.groups())
    device_code = dict(tmp)

    # device -> time_series and data preview for each sensor
    res = []
    for h3 in tree.xpath("//h3"):
        # Example h3 text content is "Tsawwassen - Duke Point Ferry Route (TWDP) - Pump and Valve Control System 02 - 24419  Device Details"
        location_name, location_code, device_name, device_id = re.match(
            r"(.*) \((.*)\).* - (.*) - (\d+).*", h3.text_content()
        ).groups()

        # Get data preview if exists
        figures = h3.xpath("./following-sibling::figure")
        if figures:
            data_preview_options = [
                extract_dp_format_id_plot_number(ele.attrib["url"]) for ele in figures
            ]

            # Get node id and device category id
            node_id, device_category_id = extract_node_id_category_id(
                figures[0].attrib["url"]
            )
        else:
            data_preview_options = []
            node_id = None
            device_category_id = None

        # Get sensors, format is [(sensor_id, sensor_name), ...]
        sensors = [
            re.match(r"(\d+)(.*)", ele.text_content()).groups()
            for ele in h3.xpath("./following-sibling::div/div[@class='sensor']")
        ]

        res.append(
            {
                "deviceId": device_id,
                "deviceName": device_name,
                "sensors": sensors,
                "locationCode": location_code,
                "locationName": location_name,
                "deviceCode": device_code[device_id],
                "searchTreeNodeId": node_id,
                "deviceCategoryId": device_category_id,
                "dataPreviewOptions": data_preview_options,
            }
        )

    with open(f"./pages/{json_filename}.json", "w") as f:
        json.dump(res, f, indent=2)
