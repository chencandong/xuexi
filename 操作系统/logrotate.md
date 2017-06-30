# Logrotate

logrotate命令用于对系统文件日记进行轮转，压缩和删除，也可以将日记发送到指定邮箱，logrotate是一个日记管理程序，用来将旧的日记文件删除（备份），并创建新的日记文件，这个过程称为转储。
查看logrotate的脚本可以发现有：

/usr/sbin/logrotate /etc/logrotate.conf

EXITVALUE=$?

if [ $EXITVALUE != 0 ]; then

    /usr/bin/logger -t logrotate "ALERT exited abnormally 
    
    with [$EXITVALUE]"
fi

exit 0

可以看到这个脚本主要就是以/etc/logrotate.conf为配置文件执行了logrotate，就是这样实现了每天执行一次的logrotate，第一次执行logrorate的时候原本的message会变为message1，会制造一个新的message来储蓄日记，第二次执行之后原本的message1会变成message2，而message会变成message.1又创建 一个新的message来储蓄日记