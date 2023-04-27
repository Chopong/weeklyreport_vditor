## Weekly Report

wangeditor 为富文本编辑器，不是很好用，建议采用 veditor的版本，源码见[github](https://github.com/Chopong/WeeklyReport_vditor)

> modified by chopong forked from CodingCrush/WeeklyReport 2023.04.01

原仓库里在 docker build 的时候遇到很多未知错误, 我做了部分修改.

原Weekly和Postgres的参数由两个文件分别控制, 我build时总是连不上数据库,后来发现是写死的, 改用环境变量传参.

* Dockerfile: 添加了一部分必要包, 老代码老报错.

* checkdb.py: 改用环境变量传参; 启动时检查数据库是否存在, 不存在则创建(可以手动创建).
* deploy/config: 改用环境变量传参

* requirements: 固定部分pip package版本号, 原库无版本, 项目代码老旧, 使得启动时各种报错代码.

* 其他: iteritem --> item 部分命令启用, 小小改动

### Build

```shell
git clone https://github.com/Chopong/WeeklyReport_vditor && \
cd WeeklyReport_editor && \
docker build -t weeklyreport:vditor .
```

### Run

```shell
docker run -d \
        --restart=unless-stopped \
        --name weeklyreport-server \
        -p 5000:5000 \
        --add-host=host.docker.internal:host-gateway
        -v /etc/localtime:/etc/localtime:ro \
        -v $PWD:/opt/weeklyreport \
        -v db_name:wr_prd \
        -v db_host:host.docker.internal \
        -v db_port:5432 \
        -v db_user:postgres \
        -v db_pass:postgres \
        weeklyreport:veditor
```

Or docker compose:

```yaml
services:
  weekly-db:
    image: postgres:9
    container_name: weeklyreport-db
    restart: unless-stopped
    ports:
      - 5432:5432
    environment:
      - POSTGRES_DB=weeklyreport
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - $PWD/deploy/postgres:/var/lib/postgresql/data
      
  weekly-server:
    image: weeklyreport:veditor
    container_name: weeklyreport-server
    restart: unless-stopped
    volumes:
      - $PWD:/opt/weeklyreport
    ports:
      - 5000:5000
    networks:
      - default
    depends_on:
      - weekly-db
    environment:
      - db_name=wr_prd
      - db_host=host.docker.internal # the docker host ip in case access denied
      - db_port=5432
      - db_user=postgres
      - db_pass=postgres
      # 更多参数,可以通过查看 /deploy/config中的变量表来定义
    extra_hosts:
      - "host.docker.internal:host-gateway" # used with host.docker.internal

# Networks
networks:
  default:
    driver: bridge
    name: database
```



参考: 1. https://wr.mcloud.fun:81/auth/login

2. https://github.com/wuchaohua/WeeklyReport
3. https://github.com/CodingCrush/WeeklyReport

---

可以在新机器上, 直接一键启动了:
docker-compose up

加入entrypoint.sh脚本:
1. 启动时先等待pg启动
2. 判断pg里是否已经有表
3. 如果没有表, 初始化表
4. 用gunicorn 启动 app

后台管理

第一次注册的用户为超级管理员，永远有登录后台的权限, 管理员可以修改其他角色

默认用户角色为`EMPLOYEE`，仅具有读写自己的周报的权限，

`MANAGER`可以读写周报，并查看本部门所有周报。而HR可以读写周报，并查看全部门所有周报。

`ADMINISTRATOR`在HR基础上增加了进入后台的功能。

`QUIT`用来标识离职后的员工，禁止其登录。
