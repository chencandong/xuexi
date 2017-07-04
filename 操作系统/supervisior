## supervisor

supervisor是一个进程管理工具，用途就是有一个进程在每时每刻不断地跑，但是这个进程又有可能由于各种原因有可能中断，当进程中断的时候洗完可以自动重新启动它，这个场景就很适合使用supervisor

### 安装supervisor

`yum install python-setuptools`

`easy_install supervisor`


验证安装成功的方法就是：在python的命令中可以成功把supervisor这个module成功导入就可以了

### 生成配置文件
`echo_supervisord_conf > /etc/supervisord.conf`

### 加载生效配置文件
`supervisorctl reload /etc/supervisord.conf ` 

###  配置program的配置文件


`[program:program]`

`directory = /dir ; 程序的启动目录command = xxx; 启动命令，可以看出与手动在命令行启动的命令是一样的`

`autostart = true ; 在 supervisord 启动的时候也自动启动`

`startsecs = 5 ; 启动 5 秒后没有异常退出，就当作已经正常启动了`

`autorestart = true ; 程序异常退出后自动重启`

`startretries = 3 ; 启动失败自动重试次数，默认是 3`

`user = leon ; 用哪个用户启动`

`redirect_stderr = true ; 把 stderr 重定向到 stdout，默认 false`

`stdout_logfile_maxbytes = 20MB ; stdout 日志文件大小，默认 50MB`

`stdout_logfile_backups = 20 ; stdout 日志文件备份数; stdout 日志文件，需要注意当指定目录不存在时无法正常启动，所以需要手动创建目录（supervisord 会自动创建日志文件`

`stdout_logfile = /data/logs/usercenter_stdout.log，这里也可以将正常输出与错误输出进行管理; `

###  可以开启supervisor web管理界面

```
;[inet_http_server] ; HTTP 服务器，提供 web 管理界面
;port=127.0.0.1:9001 ; Web 管理后台运行的 IP 和端口，如果开放到公网，需要注意安全性
;username=user ; 登录管理后台的用户名
;password=123 ; 登录管理后台的密码
```


### 使用supervisiord的命令行管理工具supervisiorctl来管理进程
```
supervisorctl status
supervisorctl stop program
supervisorctl start program
supervisorctl restart program
supervisorctl reread
supervisorctl update
```