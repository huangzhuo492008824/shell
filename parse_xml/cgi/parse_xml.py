#!/usr/bin/python
#-*- coding:utf-8 -*-

import cgi, cgitb, os
import xml.etree.ElementTree as ET

#查找给定IP是否在XML文件中
def find_ip(ip, nodes_config_list):
    for child in nodes_config_list:
        if ip == child.attrib.get("name"):
            return True
    return False

#删除已经写入的IP
def del_ip(ip, nodes_config_list):
    for child in nodes_config_list:
        if ip == child.attrib.get("name"):
            root.remove(child)
            return True

## Get pretty look 按照xml格式显示xml文档
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
        if not e.tail or not e.tail.strip():
            e.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i
    return elem

def add_element_config(root, dic):
    nodes_config = root.findall("config")
    ip_in_use = find_ip(dic["ip"], nodes_config)
    #开始增加元素config：
    if ip_in_use == False:
        tmp = ET.SubElement(root, "config", {"name":dic["ip"], "protocol":dic["protocol"] })
        tmp1 = ET.Element("param", {"name":"hostname", "value":dic["ip"]})
        tmp2 = ET.Element("param", {"name":"port", "value":dic["port"]})

        tmp.append(tmp1)
        tmp.append(tmp2)
        if dic["protocol"] == "vnc":
            tmp3 = ET.Element("parmm", {"name":"password", "value":dic["password"]})
            tmp.append(tmp3)

    # 创建 FieldStorage 的实例化
form = cgi.FieldStorage()
# 获取数据
ip = form.getvalue('ip')
protocol = form.getvalue('protocol')
port = form.getvalue('port')
#ip = "192.168.20.33"
#protocol = "vnc"
#port = "5901"
password = form.getvalue('password')
func = form.getvalue('opt')
#
filename="/var/www/cgi-bin/noauth-config.xml"
## filename_tmp = "./noauth-config.xml.bak"
#
tree = ET.parse(filename)
root = tree.getroot()
#
#
dict_ip = {"ip":ip, "protocol":protocol, "port":port, "password":password}
#
if func == 'add':
	add_element_config(root, dict_ip)
#
else:
	nodes_config = root.findall("config")
	del_ip(ip, nodes_config)

indent(root)
tree.write(filename)

print 'Content-Type: text/html\r\n\r\nKITTY' 
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
print "<h2>have added or deleted ip: %s;</h2>" % ip
print "<h2>protocol: %s;</h2>" % protocol
print "<h2>port: %s;</h2>" % port
print "<h2>password: %s;</h2>" % password
print "<h2>opt: %s;</h2>" % func
print "</body>"
print "</html>"

