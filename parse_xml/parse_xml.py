# -*- coding=utf-8 -*-
import xml.etree.ElementTree as ET


def find_ip(ip, nodes_config_list):
    for child in nodes_config_list:
        if ip == child.attrib.get("name"):
            return True
    return False

def del_ip(ip, nodes_config_list):
    for child in nodes_config_list:
        if ip == child.attrib.get("name"):
            root.remove(child)
            return True

if __name__ == "__main__":

    tree = ET.parse('./noauth-config.xml')
    root = tree.getroot()

#判断要增加的元素在不在元素树中
    ip = "192.168.20.15"
    protocol = "ssh"
    port = "22"
    ip_in_use = False

    nodes_config = tree.getroot().findall("config")

    ip_in_use = find_ip(ip,nodes_config)

#开始增加元素config：
    if ip_in_use == False:
        tmp = ET.SubElement(root, "config", {"name":ip, "protocol":protocol })
        tmp.text = "\n"
        tmp1 = ET.SubElement(tmp,"param", {"name":"hostname", "value":ip })

        tmp2 = ET.SubElement(tmp,"param", {"name":"port", "value":port})

        nodes_config.append(tmp)
    del_ip("25-ssh", nodes_config)
    tree.write("xml_out002.xml")

