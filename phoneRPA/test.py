import os
import xml.etree.ElementTree as ET
import re
# os.system("adb shell uiautomator dump /sdcard/ui.xml")
# os.system("adb pull sdcard/ui.xml")

tree = ET.parse('ui.xml')
root = tree.getroot()

Nodes = root.findall(".//*[@content-desc='更多']")
position = 0
if len(Nodes ):
    position = Nodes[0].attrib["bounds"]
print(re.findall(r"\d+",position))
    