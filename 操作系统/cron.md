
## cron系统配置文件的路径是什么

**定义与系统相关的crontab作业：**
* /etc/crontab
* /etc/cron.d中的任何文件
* /etc/cron.hour,/etc/cron.daily,/etc/cron.weekly,/etc/cron.mouthly 

**定义针对用户的crontab任务**
针对特定用户的配置文件，针对用户的crontab集合通常放在/var/spool/cron中，同样建议使用crontab命令创建

分别可以使用/etc/cront.allow和/etc/cront.deny可以允许和拒绝用户访问cron任务，当/etc/cront.allow这个文件存在的时候，/etc/cront.deny不生效，当/etc/cront.allow不存在，/etc/cront.deny存在的时候，/etc/cront.deny生效，当两个文件都不存在的时候，只有root用户可以使用crontab命令


## cron的时间描述中-代表什么意思，/代表什么意思
-代表为连续取值的意思，/代表的是定义步长的意思

crontab的作业命令由单行的固定格式的文本构成，一般分为三个部分：

1. 执行频率 定义周期性时间，以空格分隔的五个字段代表分钟，小时，日期，月份，周，这个也代表了cron任务执行的最小颗粒度为分钟，但是当我们需要运行的周期为秒级的时候建议使用循环语句，配置sleep达到妙级的周期性任务
2. crontab所有者，运行任务的用户身份，系统级的crontab必须具备这个字段，用户级的crontab不需要这个字段，是否具备用户名是系统级和用户级cron的唯一差异
3. 执行命令或者脚本 

## @reboot会在什么时候执行
@reboot        Run once, at startup

根据该定义可以知道@reboot只会执行一次，在系统启动的时候运行，其他相似的的类似可以参考如下：

* @yearly:         Run once a year, "0 0 1 1 *". 
* @annually:      (same as @yearly) 
* @monthly:       Run once a month, "0 0 1 * *". 
* @weekly:        Run once a week, "0 0 * * 0". 
* @daily:           Run once a day, "0 0 * * *". 
* @midnight:      (same as @daily) 
* @hourly:         Run once an hour, "0 * * * *".

##  cron的任务的最小颗度为分钟，如何使用cron实现没分钟跑两次，例如分别在0s和30s的运行的任务

一般使用脚本的循环语句或者sleep语句进行控制，例如

* * * * * * date "+%H:%M:%S" >>/tmp/time.txt
* * * * * * sleep 30； date "+%H:%M:%S" >>/tmp/time.txt

业可以在脚本中使用循环+sleep来达到秒级的任务作业