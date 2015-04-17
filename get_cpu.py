import time,os
import sys
import MySQLdb

def get_ip_extend():
        ip_all = os.popen('ifconfig').read().split('\n\n')
        for i in ip_all:
                if i.find('eth')!=-1:
                        ipaddress = i.split('\n')[1].split(':')[1].split(' ')[0]
                        if ipaddress.find('172') == -1:
                                net_device = i.split(' ')[0]
                                return net_device,ipaddress
        return None

def get_hostname():
        return os.popen('hostname').read().split('\n')[0]

def get_date():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

def get_cpu_memory():
        '''
        return idle memory string MB
        return cpu_use % string
        '''
        top_cmd = os.popen('top -bi -n 2 -d 0.02').read().split('\n\n\n')[1]
        memory_idle = "%.2f"%(float(top_cmd.split('\n')[3].split(',')[2].split('k')[0])/1024)
        cpu_use = "%.2f"%(100.00-float(top_cmd.split('\n')[2].split(',')[3].split('%')[0]))
        return cpu_use,memory_idle

######################## get localdisk ######################
def get_localdisk():
        df_cmd = os.popen('df -l').read().split('\n')[1]
        idle_str = ' '.join(df_cmd.split())

        idle_MB = "%.2f"%(float(idle_str.split(' ')[3])/1024)
        return idle_MB

####################get net ################

def     rx():
        ifstat = open('/proc/net/dev').readlines()
        for interface in  ifstat:
                if INTERFACE in interface:
                        stat = float(interface.split()[1])
                        STATS[0:] = [stat]

def     tx(INTERFACE):
        ifstat = open('/proc/net/dev').readlines()
        for interface in  ifstat:
                if INTERFACE in interface:
                        stat = float(interface.split()[1])
                        STATS[0:] = [stat]

def     tx(INTERFACE):
        ifstat = open('/proc/net/dev').readlines()
        for interface in  ifstat:
                if INTERFACE in interface:
                        return float(interface.split()[9])


def get_net_tx(INTERFACE):

        pre_byte = tx(INTERFACE)
        time.sleep(1)
        post_byte = tx(INTERFACE)

        print 'pre_byte',pre_byte
        print 'post_byte',post_byte
        return round((post_byte*1.00-pre_byte)/1024,2)

#######################  running ping cmd ###########
def run_ping(ip, times):

        os.popen('ping %s -c %d' % (ip,times))

if __name__ == '__main__':
        pre_byte = -1
#set collect time:
        collect_time=120
#       INTERFACE = 'eth0'
        ip = '192.168.3.25'
        run_ping(ip, 10)

        while True:
                INTERFACE,IPADDRESS = get_ip_extend()
        #       print get_net_tx(INTERFACE),"KB"
                if pre_byte == -1:
                        pre_byte=tx(INTERFACE)
                        time.sleep(1)
                        post_byte=tx(INTERFACE)
                        net_rate=round((post_byte*1.00-pre_byte)/1024,2)
#                       print 'TX:',net_rate,'KB/s'
                        pre_byte=post_byte
                else:
                        post_byte=tx(INTERFACE)
                        net_rate=round((post_byte*1.00-pre_byte)/(1024*collect_time),2)
#                       print '%s TX:' % INTERFACE,net_rate,'KB/s'
                        pre_byte=post_byte
                print '#######################################################'

                hostname = get_hostname()
                cpu_use,memory_idle =  get_cpu_memory()
                date =  get_date()
                local_disk = get_localdisk()

                print date,INTERFACE,IPADDRESS,hostname,cpu_use,memory_idle,net_rate,local_disk

                conn = MySQLdb.connect(host='192.168.20.124', user='root', passwd='123.com', port=3306)
                cursor = conn.cursor()

#               print type(hostname),type(IPADDRESS),type(cpu_use),type(date)
                sql_processor = "null, '%s', '%s', '%s', '%s', 'Processor', '"%(hostname, IPADDRESS, cpu_use, date)+ "% Processor Time', '_Total'"
#               print 'processor:', sql_processor
                sql_memory = "null, '%s', '%s', '%s', '%s', 'Memory', 'Available MBytes', ''"%(hostname, IPADDRESS, memory_idle, date)
                sql_disk = "null, '%s', '%s', '%s', '%s', 'LogicalDisk', '"%(hostname, IPADDRESS, local_disk, date)+ "% Free Space', '_Total'"
                sql_net = "null, '%s', '%s', '%s', '%s', 'Network Interface', 'Bytes Total/sec', ''"%(hostname, IPADDRESS, net_rate, date)

#               print "INSERT INTO privatecloud_hardware.performance VALUES(%s);" % sql_processor
                insert = cursor.execute("INSERT INTO privatecloud_hardware.performance VALUES(%s);" % sql_processor)
                insert = cursor.execute("INSERT INTO privatecloud_hardware.performance VALUES(%s);" % sql_memory)
                insert = cursor.execute("INSERT INTO privatecloud_hardware.performance VALUES(%s);" % sql_disk)
                insert = cursor.execute("INSERT INTO privatecloud_hardware.performance VALUES(%s);" % sql_net)
                conn.commit()


                cursor.close()
                conn.close()
                  time.sleep(collect_time)


#if len(sys.argv) > 1:
#       INTERFACE = sys.argv[1]
#else:
#       INTERFACE = 'eth0'
#STATS = []
#print 'Interface:',INTERFACE
#
#def    rx():
#       ifstat = open('/proc/net/dev').readlines()
#       for interface in  ifstat:
#               if INTERFACE in interface:
#                       stat = float(interface.split()[1])
#                       STATS[0:] = [stat]
#
#def    tx():
#       ifstat = open('/proc/net/dev').readlines()
#       for interface in  ifstat:
#               if INTERFACE in interface:
#                       stat = float(interface.split()[9])
#                       STATS[1:] = [stat]
#
#print  'In                     Out'
#rx()
#tx()
#
##while True:
#time.sleep(1)
#rxstat_o = list(STATS)
#rx()
#tx()
#RX = float(STATS[0])
#RX_O = rxstat_o[0]
#TX = float(STATS[1])
#TX_O = rxstat_o[1]
#RX_RATE = round((RX - RX_O)/1024,3)
#TX_RATE = round((TX - TX_O)/1024,3)
#print RX_RATE ,'KB             ',TX_RATE ,'KB'

