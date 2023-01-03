# Docker로 Redis Cluster 구성하기 

## Announce IP

### Host IP 확인

- docker가 올라가는 host 에서 
```bash
> ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: bond0: <BROADCAST,MULTICAST,MASTER> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 02:3f:24:8f:f3:63 brd ff:ff:ff:ff:ff:ff
3: dummy0: <BROADCAST,NOARP> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether aa:5d:44:75:91:7c brd ff:ff:ff:ff:ff:ff
4: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:15:5d:0a:f3:55 brd ff:ff:ff:ff:ff:ff
    inet 172.19.155.82/20 brd 172.19.159.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::215:5dff:fe0a:f355/64 scope link 
       valid_lft forever preferred_lft forever
5: tunl0@NONE: <NOARP> mtu 1480 qdisc noop state DOWN group default qlen 1000
    link/ipip 0.0.0.0 brd 0.0.0.0
6: sit0@NONE: <NOARP> mtu 1480 qdisc noop state DOWN group default qlen 1000
    link/sit 0.0.0.0 brd 0.0.0.0

```
 - 여기서 eth0 의 주소 172.19.155.82 를 announce ip로 사용.

### redis-stack.conf

- 아래 사항을 추가
```
cluster-announce-ip 172.19.155.82
```


## 컨테이너는 IP 지정

```yml
  redis-node-1:
    image: redis/redis-stack-server:6.2.2-v5
    container_name: redis-master-2
    volumes:
      - ./redis_7002.conf:/etc/redis-stack.conf
      - ./logs:/data/redis
    command: redis-server /etc/redis-stack.conf
    ports:
      - 17002:17002
      - 7002:7002
```

## Test

- `/data/redis` 에 직전 conf 가 있는 경우 문제발생함. 지우고 컨테이너 up 
- 아래와 같이 동작 
  
```bash
$ redis-cli -p 7001 -c
127.0.0.1:7001> cluster info
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:9
cluster_size:3
cluster_current_epoch:9
cluster_my_epoch:1
cluster_stats_messages_ping_sent:257
cluster_stats_messages_pong_sent:262
cluster_stats_messages_sent:519
cluster_stats_messages_ping_received:254
cluster_stats_messages_pong_received:257
cluster_stats_messages_meet_received:8
cluster_stats_messages_received:519
127.0.0.1:7001> set xkey 1
-> Redirected to slot [14157] located at 172.19.155.82:7003
OK
172.19.155.82:7003> get xkey
"1"
172.19.155.82:7003> set xfwef 1234
-> Redirected to slot [1223] located at 172.19.155.82:7001
OK
172.19.155.82:7001> get xfwef
"1234"
172.19.155.82:7001>
172.19.155.82:7001> module list
name,graph,ver,20815,name,search,ver,20409,name,timeseries,ver,10616,name,ReJSON,ver,20009,name,bf,ver,20217
172.19.155.82:7001> 
```



```bash


```