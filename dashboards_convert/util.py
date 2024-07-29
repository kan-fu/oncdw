import re


def extract_dp_format_id_plot_number(url: str) -> tuple[int, int]:
    return tuple(
        map(
            int,
            re.search(r"dataProductFormatId=(\d+)&plotNumber=(\d+)", url).groups(),
        )
    )


def extract_node_id_category_id(url: str) -> tuple[int, int]:
    return tuple(
        map(
            int,
            re.search(r"searchTreeNodeId=(\d+)&deviceCategoryId=(\d+)", url).groups(),
        )
    )
