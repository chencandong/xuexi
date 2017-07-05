### 关于dos攻击的问题
如何确定是否受到dos攻击

```
执行netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -n
```

连接数过多的时候就有可能受到了dos攻击

### 使用iptables来防止攻击
```
执行netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -n

sysctl -w net.ipv4.ip_forward=1 &>/dev/null

sysctl -w net.ipv4.tcp_syncookies=1 &>/dev/null#打开 syncookie （轻量级预防 DOS 攻击）

sysctl -w net.ipv4.netfilter.ip_conntrack_tcp_timeout_established=3800 &>/dev/null#设置默认 TCP 连接最大时长为 3800 秒（此选项可以大大降低连接数）

sysctl -w net.ipv4.ip_conntrack_max=300000 &>/dev/n#设置支持最大连接树为 30W（这个根据你的内存和 iptables 版本来，每个 connection 需要 300 多个字节）

iptables -N syn-flood

iptables -A INPUT -p tcp --syn -j syn-flood

iptables -I syn-flood -p tcp -m limit --limit 3/s --limit-burst 6 -j RETURN

iptables -A syn-flood -j REJECT#防止SYN攻击 轻量级预防

iptables -A INPUT -i eth0 -p tcp --syn -m connlimit --connlimit-above 15 -j DROP

iptables -A INPUT -p tcp -m state --state ESTABLISHED,RELATED -j ACCEPT#防止DOS太多连接进来,可以允许外网网卡每个IP最多15个初始连接,超过的丢弃
```

## 二、使用DDoS deflate

DDoS deflate是一款免费的用来防御和减轻DDoS攻击的脚本。它通过netstat监测跟踪创建大量网络连接的IP地址，在检测到某个结点超过预设的限 制时，该程序会通过APF或IPTABLES禁止或阻挡这些IP.
DDoS deflate官方网站：http://deflate.medialayer.com/
```
1、安装DDoS deflate
wget http://www.inetbase.com/scripts/ddos/install.sh   //下载DDoS  deflate
chmod 0700 install.sh    //添加权限
./install.sh            //执行
卸载
wget http://www.inetbase.com/scripts/ddos/uninstall.ddos
chmod 0700 uninstall.ddos
./uninstall.ddos
2、配置DDoS deflate
下面是DDoS deflate的默认配置位于/usr/local/ddos/ddos.conf ，内容如下：
##### Paths of the script and other files
PROGDIR="/usr/local/ddos"
PROG="/usr/local/ddos/ddos.sh"
IGNORE_IP_LIST="/usr/local/ddos/ignore.ip.list"  //IP地址白名单
CRON="/etc/cron.d/ddos.cron"    //定时执行程序
APF="/etc/apf/apf"
IPT="/sbin/iptables"
##### frequency in minutes for running the script
##### Caution: Every time this setting is changed, run the script with --cron
#####          option so that the new frequency takes effect
FREQ=1   //检查时间间隔，默认1分钟
##### How many connections define a bad IP? Indicate that below.
NO_OF_CONNECTIONS=150     //最大连接数，超过这个数IP就会被屏蔽，一般默认即可

##### APF_BAN=1 (Make sure your APF version is atleast 0.96)
##### APF_BAN=0 (Uses iptables for banning ips instead of APF)
APF_BAN=1        //使用APF还是iptables。推荐使用iptables,将APF_BAN的值改为0即可。

##### KILL=0 (Bad IPs are'nt banned, good for interactive execution of script)
##### KILL=1 (Recommended setting)
KILL=1   //是否屏蔽IP，默认即可

##### An email is sent to the following address when an IP is banned.
##### Blank would suppress sending of mails
EMAIL_TO="root"   //当IP被屏蔽时给指定邮箱发送邮件，推荐使用，换成自己的邮箱即可
##### Number of seconds the banned ip should remain in blacklist.
BAN_PERIOD=600    //禁用IP时间，默认600秒，可根据情况调整
用户可根据给默认配置文件加上的注释提示内容，修改配置文件。
查看/usr/local/ddos/ddos.sh文件的第117行
netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr > $BAD_IP_LIST
修改为以下代码即可！
netstat -ntu | awk '{print $5}' | cut -d: -f1 | sed -n '/[0-9]/p' | sort | uniq -c | sort -nr > $BAD_IP_LIST
```