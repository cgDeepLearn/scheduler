# k3s部署scheduler

## 安装k3s及其准备

### 关闭防火墙

```shell
systemctl disable firewalld --now
```

### 检查部署机器的主机名

```shell
hostname
```

如果没有设置主机名，输入如下命令:

```shell
# test为设置的主机名
hostnamectl set-hostname test
# 设置后输入hostname命令查看确认
hostname
```

### 设置时区

```shell
# 输入date 查看机器的系统时间
date
# Mon Oct 11 16:33:56 CST 2021
# 如果不是中国时区, 如下修改：
ln -s /usr/share/zoneinfo/PRC /etc/localtime
```

### 数据盘

会使用到[longhorn](https://www.rancher.cn/longhorn/)来做存储

- 简单点: 

```shell
mkdir -p /data/longhorn
```

- 复杂点
```shell
# 需要根据实际情况修改设备和uuid
fdisk -l
mkfs.ext4 /dev/vdb
ls -l /dev/disk/by-uuid
vi /etc/fstab
UUID=51c11733-47de-49de-8a20-7f19aa96d3ad /data/longhorn ext4 defaults 0 0

mkdir -p /data/longhorn
mount /data/longhorn
```

### 安装k3s

```shell
curl -sfL http://rancher-mirror.cnrancher.com/k3s/k3s-install.sh | INSTALL_K3S_MIRROR=cn sh -s - --disable local-storage
# 配置镜像mirrors
cat > /etc/rancher/k3s/registries.yaml << EOF
mirrors:
  docker.io:
    endpoint:
      - "https://mirror.baidubce.com"
      - "https://docker.mirrors.ustc.edu.cn/"
      - "https://registry-1.docker.io"
EOF
```

### 安装配置longhorn

```shell
# 安装依赖
yum install -y iscsi-initiator-utils nfs-utils jq
# 环境检查
curl -sSfL https://raw.githubusercontent.com/longhorn/longhorn/v1.1.1/scripts/environment_check.sh | bash
# 安装
curl -Lo longhorn.yaml https://raw.githubusercontent.com/longhorn/longhorn/v1.1.1/deploy/longhorn.yaml
# 修改default-data-path、annotations、is-default-class、reclaimPolicy、numberOfReplicas
vi longhorn.yaml
    default-data-path: /data/longhorn
...
  storageclass.yaml: |
    kind: StorageClass
    apiVersion: storage.k8s.io/v1
    metadata:
      name: longhorn
      annotations:
        storageclass.kubernetes.io/is-default-class: "true"
    provisioner: driver.longhorn.io
    allowVolumeExpansion: true
    reclaimPolicy: Retain
    volumeBindingMode: Immediate
    parameters:
      numberOfReplicas: "1"
      staleReplicaTimeout: "2880"
      fromBackup: ""

kubectl apply -f longhorn.yaml
kubectl get storageclass
```

## 部署scheduler

### 创建名字空间

```kubectl create ns scheduler```

### 拉取镜像

```shell
# 拉取redis 和postgres 数据库镜像
ctr i pull docker.io/library/redis:alpine
ctr i pull docker.io/library/postgres:12.5

# 拉取scheduler镜像(之前推送到了dockerhub)
ctr i pull docker.io/cgdeeplearn/scheduler_sbackend:0.1.3
ctr i pull docker.io/cgdeeplearn/scheduler_smgr:0.1.3
ctr i pull docker.io/cgdeeplearn/scheduler_sworker:0.1.3
```

### 编写yaml文件

- db: [db.yaml](.k3s/db.yml)
- scheduler: [scheduler.yaml](.k3s/scheduler.yml)

将yaml文件移动到k3s目录
```shell
# 创建项目目录
mkdir -p /var/lib/rancher/k3s/server/manifests/my-scheduler
#移动yml文件到该目录
mv db.yml scheduler.yml /var/lib/rancher/k3s/server/manifests/my-scheduler
```

### 运行db

```shell
cd /var/lib/rancher/k3s/server/manifests/my-scheduler
kubectl apply -f db.yml
```

- 查看pod

```shell
# 可以看到应用db.yml后创建了sredis和spostgres两个pod
kubectl get pod -n scheduler
# NAME                         READY   STATUS    RESTARTS   AGE
# sredis-699cdb4d44-fvtnm      1/1     Running   0          11m
# spostgres-7bffcf5657-rzbn8   1/1     Running   0          11m
```

### 初始化建表sql

建表sql: [backend.sql](scripts/backend.sql)

进入该sql目录，将sql copy到pod内并执行，当然也可以通过db连接工具连接后，执行该sql
```shell
kubectl cp backend.sql scheduler/spostgres-7bffcf5657-rzbn8:/tmp
```

### 运行scheduler

```shell
cd /var/lib/rancher/k3s/server/manifests/my-scheduler
kubectl apply -f scheduler.yml
# 查看pod
kubectl get pod -n scheduler
# NAME                         READY   STATUS    RESTARTS   AGE
# sredis-699cdb4d44-fvtnm      1/1     Running   0          11m
# spostgres-7bffcf5657-rzbn8   1/1     Running   0          11m
# smgr-599dd6b5db-dvrtd        1/1     Running   0          2m
# sworker2-6fdfdf95f5-dh2pd    1/1     Running   0          2m
# sworker1-86f5498bbb-sbnkc    1/1     Running   0          2m
# sbackend-6d695b597b-bqzjg    1/1     Running   0          2m

# 进入某个pod查看
kubectl exec -it -n scheduler sbackend-6d695b597b-bqzjg -- sh
```

### postman 测试接口

同[docker-compose部署](README.md) 后的步骤

#### 1. 获取任务列表

```shell
GET http://your-host:30001/tasks   (Headers: Content-Type:application/json; charset=utf-8)

RESPONSE:
{
    "data": [],
    "success": true,
    "message": "Succeed"
}
```

....


