## socket的类型
套接字格式：socket使用给定的地址族，套接字类型，协议编号（默认为0来创建套接字），关于socket的常用的类型有：

1. socket.AD_INET 服务器之间网络通信
2. socket.AF_INET6 用于ipv6
3. socket.SOCK_STREAM  流式socket，for TCP
4. socket.SOCK_DREAM 数据报式socket，for UDP
5. socket.RAW 原始套接字，普通的套接字无法处理ICMP，IGMP等网络保温，而SOCK_RAW可以，其次，RAW也可以处理特殊的ipv4的报文

创建tcp的socket：s=socket.socket(sockert.AF_INET,socket.SOCK_STREAM)

创建udp的socket：s=socket.socket(socket.AF_INET,socket_DGRAM)

## socket的函数：

tcp发送数据的时候，已经建立好了tcp连接，所以不需要指定地址，udp是面向无连接的，每次发送要指定是发送给谁，服务端与客户端不能直接发送列表，元祖和字典，需要字符串花repr(date)

s.bind()  将套接字绑定到地址，以元祖（host，port）的形式表达地址

s.listen(backlog)  开始监听tcp的传人连接，backlog表示的是操作系统可以挂起的最大连接数量，至少为1

s.accept 接受tcp连接并且返回(conn,address)其中conn是新的套接字对象，可以用来接受和发送数据，address是连接客户端的地址

客户端的函数有：

s.connect(address)一般address的格式为元祖（hostname，port），如果连接出错，放回socket.err的错误

s.connect_ex(address) 功能与connect（address）相同，但是成功返回0，失败返回errno的值

公共socket的函数有：

s.recv(bufsize[,flag])接受tcp套接字的数据，数据已字符串的形式返回，buffsize是指定要接受的最大数据量，flag提供有关信息的其他消息，通常可以忽略

s.send(string[,flag])发送tcp的数据，将string中的数据发送到连接的套接字，返回值是要发送的字节数量

s.sendall：完整发送tcp的数量，将string中的数据发送到连接的套接字，返回值是要发送到的字节数量，该数量可能小于string的字节大小

s.close：关闭套接字

## socket的编程思想

1. 创建套接字，绑定套接字到本地的ip与端口（*s=socket.socket(socket.AF_INET,socket.SOCKET_STREAM),s.bind()*）
2. 开始监听连接（*s.listen(5)*）
3. 进入循环，不断接受客户端的连接请求 （*s.accept()*）
4. 然后接收传来的数据，并发送给对方数据 （*s.recv(),s.sendall()*）
5. 传输完毕，关闭套接字
