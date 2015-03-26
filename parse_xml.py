# -*- coding=utf-8 -*-

import xml.etree.ElementTree as ET

if __name__ == "__main__":

    tree = ET.parse('./noauth-config.xml')
    root = tree.getroot()

#判断要增加的元素在不在元素树中
    ip = "192.168.20.15"
    protocol = "ssh"
    port = "22"
    ip_in_use = False

    nodes_config = tree.getroot().findall("config")

    for child in nodes_config:
        print child.tag,child.attrib
        if ip == child.attrib.get("name"):
            print "ip is in use!"
            ip_in_use=True
            break

#开始增加元素config：
    if ip_in_use == False:
        print "hehe"
        tmp = ET.SubElement(root, "config", {"name":"192.168.20.15", "protocol":"ssh"})
        tmp.text = "\n"
        tmp1 = ET.SubElement(tmp,"param", {"name":"hostname", "value":"192.168.20.15"})

        tmp2 = ET.SubElement(tmp,"param", {"name":"port", "value":"22"})

        nodes_config.append(tmp)
    tree.write("xml_out002.xml", encoding="utf-8",xml_declaration=True)
