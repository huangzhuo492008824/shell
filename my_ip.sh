#/bin/sh

#这是一个获取和修改CentOS6.5的脚本程序，包括两个函数：Get_ip()和Change_ip()
#ETHCONF=./tmp
ETHCONF=/etc/sysconfig/network-scripts/ifcfg-eth0
DIR=/data/backup/`date +%Y%m%d`
#NEW_IP=192.168.20.5
#NEW_GATEWAY=192.168.20.1
#NEW_MASK=255.255.255.0
#NEW_DNS=8.8.8.114
NEW_IP=$1
NEW_GATEWAY=$2
NEW_MASK=$3
NEW_DNS=$4

function Get_ip()
{
 old_ip=$(ifconfig | awk '/eth/{inter=$1;getline;sub(/inet addr:/,"");print inter,$1}'|awk '{print $2}')
# old_gateway=$(netstat -r|grep default|cut -f 10 -d ' ') 
 old_gateway=192.168.20.5
 old_mask=$(ifconfig | grep 'Mask:'| grep -v '127.0.0.1' | cut -d: -f4 | awk '{ print $1}')
 if [ -f /etc/resolv.conf ];
 then
   dns=`awk '/^nameserver/{print $2}' /etc/resolv.conf `
 fi
 echo "Old ip address is: $old_ip; $old_gateway; $old_mask; $dns"
 
}


function Change_ip()
{
#判断备份目录是否存在，中括号前后都有空格，！叹号在shell表示相反的意思#
if
 [ ! -d $DIR ];then

 mkdir -p $DIR

fi
 cp $ETHCONF $DIR
 grep "dhcp" $ETHCONF
if
 [ $? -eq 0 ];then
 sed -i 's/dhcp/static/g' $ETHCONF
fi 
sed -i "/IPADDR/d" $ETHCONF
sed -i "/NETMASK/d" $ETHCONF
sed -i "/GATEWAY/d" $ETHCONF
sed -i "/DNS/d" $ETHCONF

echo -e "IPADDR=$NEW_IP\nNETMASK=$NEW_MASK\nGATEWAY=$NEW_GATEWAY\nDNS1=$NEW_DNS" >> $ETHCONF
 echo "success" 
}
Get_ip
Change_ip
service network restart
