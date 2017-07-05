###  安装elasticsearch
```
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.4.3.tar.gz

tar zxvf elasticsearch-5.4.3.tar.gz

cd  elasticsearch-5.4.3.tar.gz
```

### 启动运行elasticsearch

```
./bin/elasticsearch -d ;配置文件为elasticsearch.yml中的network.host（注意：后要空一格）
```

1. elasticsearch中默认安装之后使用的内存为1GB，修改elastucsearch的堆内存，最简单的一个方法就是制定ES_HEAP_SIZE的环境变量

`export ES_HEAP_SIZE=10g`

2. 或者在启动的时候使用命令行的参数的形式，在程序启动的时候把内存大小传递给他
./bin/elasticsearch  -Xmx10g -Xms10g
发现第一种方式不再支持了，只能够使用第二种方式

### 关闭elasticsearch
1. 可以杀死进程
2. 调用相对应的elasticsearch的接口
curl -XPOST 'http：//localhost:9200/_shutdown'

打开终端调用"http://localhost:9200/?pretty"
能够正常打开表示elasticsearch可以正常启动和运行

###  安装最新版中的一些坑
1. 首先需要对系统进行调优 主要在于ulimit -n和ulimit-u这两个值
2. 然后需要最/etc/security/limits.d/90-nproc.conf修改其中的*          soft    nproc     2048
3. 需要修改内核参数为：sysctl -w vm.max_map_count=262144（临时生效）
4. centos中需要关闭下列的两个参数
```
bootstrap.memory_lock: false
bootstrap.system_call_filter: false
```



### elasticsearch配置文件详解
```
cluster.name:elasticsearch  配置es集群的名字
node.name  配置节点的名字
node.master  配置该节点是否有资格选举成为master，默认为true
node.data 指定该节点是否存储索引，默认为true
index.number_of_replicas 设置默认副本索引分片个数，默认为5片
index.number_of_shards   设置默认索引分片个数，默认为1个副本
path.conf:配置文件的存储路径默认为es根目录下的work文件
path.work 临时文件的存储路径，默认为es根目录下的work文件
path.log 设置日记文件的存放路径，默认为es根目录下的log文件
path.plugin 设置插件的存放路径，默认为es根目录下plugin的文件

bootstrap.mlockall 设置为true来锁定内存，当jvm开始使用swap的时候es的效率会变低，所以需要保证不使用swap，linux下可以使用ulinit -l unlimited命令
network.bind.host  设置绑定的ip地址，默认为0.0.0.0
network.publish_host：配置其他节点与该节点交互的ip地址
network.host 是用来配置bind_host和public上面两个参数的

transport.tcp.port:9300 配置节点之间交互的tcp端口，默认为9300
transport.tcp.compress：true 配置压缩传输的数据，默认为false，不压缩
http.port 9200  默认对外的http端口
http.enabled:false 是否使用http协议来对外提供服务，默认为true，开启
gateway.type:local local即为本地文件系统，hadoop的HDFS和amazon的s3服务器
gateway.recover_afer_nodes:1 配置集群中n个节点启动时候进行数据恢复，默认为1
gateway.recover_after_nodes:5m 配置初始化集群恢复进程的超时时间
cluster.routing.allocation_initial_primaries_recoveries:
初始化数据恢复的时候，并发恢复线程的个数，默认为4

discovery.zen.minimum_master_node:1 配置这个参数来保证集群中的节点可以知道它有master资格的节点，默认为1，对于大的集群，可以配置为大一点的集群

discovery.zen.ping.multicast.enable 配置是否打开多播发现节点，可以通过这些节点来自动发现加入集群的节点

discovery.zen.ping.unicast.host:["host",host:port]

```

### es中查询的漫日记参数配置
```
index.search.slowlog.level: TRACE
index.search.slowlog.threshold.query.warn: 10s
index.search.slowlog.threshold.query.info: 5s
index.search.slowlog.threshold.query.debug: 2s
index.search.slowlog.threshold.query.trace: 500ms

index.search.slowlog.threshold.fetch.warn: 1s
index.search.slowlog.threshold.fetch.info: 800ms
index.search.slowlog.threshold.fetch.debug:500ms
index.search.slowlog.threshold.fetch.trace: 200ms
```


### 由于elasticsearch5版本以后不支持直接使用插件工具安装head管理插件，直接使用docker容器来进行管理
添加yum源，安装dockera-engine
```
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
```
拉取docker的管理软件head的镜像
```
docker  pull jeanberu/elasticsearch-head:5

docker run -p 9100:9100 mobz/elasticsearch-head:5
```
这个时候打开9100端口的时候就可以直接连接elasticsearch查看集群的情况

### 查看集群健康的接口和使用head插件查看es集群的健康情况
`curl 127.0.0.1：9200/_cluster/health?pretty`

使用这个接口可以查看集群的健康情况

elasticsearch无法连接集群的情况需要修改配置：
```
http.cors.enabled: true
http.cors.allow-origin: "*"
```
重启es和head的docker容器就可以重启连接上来，默认分片为5

### 安装kopf插件来管理es集群
目前kopf支持到es2.x版本，因此kopf不支持es5.0以上的集群，解决方法
* 使用elasticsearch-head插件来使用
* 需要手动修改kopf的源码来兼容
详情可以参考[kops修改][1]

在github中找到这个地址[kopf][2]下载相对应版本的zip，进行解压

## elasticsearch常见的接口统计
```
curl -XPUT 'localhost:9200/twitter/tweet/1?pretty' -H 'Content-Type: application/json' -d'
{
    "user" : "kimchy",
    "post_date" : "2009-11-15T14:12:12",
    "message" : "trying out Elasticsearch"
}
'

curl -XPUT 'localhost:9200/twitter/tweet/2?pretty' -H 'Content-Type: application/json' -d'
{
    "user" : "chencandong",
    "post_date" : "2017-07-05T18:52:00",
    "message" : "this is chencandong twitter"
}
'
```
#### 计算集群中文档的数量可以使用
'''
curl -XGET 'http://localhost:9200/_count?pretty' -d '
{
    "query": {
        "match_all": {}
    }
}
'
'''
这个与`curl -XGET 'http://localhost:9200/_count?pretty'`的效果是一样的
如果需要返回客户端的头部信息的时候可以加上-i来进行操作


#### 检索文档：
一般来讲，使用put或者post来存储数据，使用GET来检索数据，使用HEAD来检查文档是否存在，使用DELETE来删除相对应得文档，想要更新已经存在的文档，只需要重新再put文档

使用GET的方式来进行检索 
`GET /index/_type/_id？pretty`的方式可以检索出我们想要到的数据

#### 轻量搜索
使用_search进行最简单的搜索，请求所有的内容，返回的结果放在hits数组中，一个搜索默认返回十条结果，例如：
`10.249.43.100:9200/ccd/employee/_search?pretty`

#### 使用高亮搜索
搜索的路径为_search?q=key:value,例如：
`10.249.43.100:9200/ccd/employee/_search?q=age:32&pretty`

####  通过查询表达式搜索
领域特定语言DSL，指定一个json请求，可以重写之前age等于32的请求
```
{
	"query" : {

			"match":{
				"age"：32
 			}
     }
}
```
#### 更加复杂的搜索可以例如must，bool，match，filter等等可以查阅一下文档
#### 全文搜索和短语搜索
全文搜索和短语搜索的不同在于match和match_pharse的不同

###高亮搜索的例子
```
{
    "query" : {
        "match_phrase" : {
            "about" : "rock climbing"
        }
    },
    "highlight": {
        "fields" : {
            "about" : {}
        }
    }
}

匹配到的字符串会以<em></em>标签的方式封装
```

[1]:https://stackoverflow.com/questions/41340749/installation-of-kopf-plugin-for-elasticsearch-5-1-1
[2]:https://github.com/lmenezes/elasticsearch-kopf

