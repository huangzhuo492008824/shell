#!/usr/bin/python
#coding=utf-8

print "Content-type:text/html\r\n\r\nhaha"
# CGI处理模块
import cgi, cgitb, os

# 创建 FieldStorage 的实例化
form = cgi.FieldStorage() 
# 获取数据
ip = form.getvalue('ip')
protocol = form.getvalue('protocol')
port = form.getvalue('port')

content = '''
    <config name="%s" protocol="%s">
        <param name="hostname" value="%s" />
        <param name="port" value="%s" />
    </config>
''' % (ip, protocol, ip, port)

filename = '/etc/guacamole/noauth-config.xml'
tmp = '/etc/guacamole/noauth-config.xml.bak2'
with open(filename) as f:
    lines = f.readlines()
#    print lines,
    curr = lines[:-1]
f = open(tmp, 'w')
f.writelines(curr)
f.write(content)
f.write(lines[-1])
f.close()
os.rename(tmp, filename)

print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
print "<h2>ip: %s; protocol: %s; port: %s</h2>" % (ip, protocol, port)
print "</body>"
print "</html>"
