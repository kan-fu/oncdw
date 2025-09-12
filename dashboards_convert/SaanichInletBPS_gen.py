from util import template_ferry_gen

html_filename = "SaanichInletBPS"
json_filename = "Saanich_Inlet_BPS"

# The html file is mal-formatted. I need to temporarily change line 225 at util.py from
# `for ele in h3.xpath("./following-sibling::div/div[@class='sensor']")`
# to
# `for ele in h3.xpath("./following-sibling::section//div[@class='sensor']")`
template_ferry_gen(html_filename, json_filename)
