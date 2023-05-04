## Weekly Report

wangeditor 为富文本编辑器，不是很好用，建议采用 veditor的版本，源码见[github](https://github.com/Chopong/WeeklyReport_vditor)

> modified by chopong forked from CodingCrush/WeeklyReport

原仓库里在 docker build 的时候遇到很多未知错误, 我做了部分修改.

原Weekly和Postgres的参数由两个文件分别控制，我build时总是连不上数据库，后来发现是另一个文件，而且方法是写死的，于是改用环境变量传参。

* Dockerfile: 添加了一部分必要包, 旧代码总报错.
* checkdb.py: 改用环境变量传参; 启动时检查数据库是否存在, 不存在则创建(可以手动创建).
* deploy/config: 改用环境变量传参
* requirements: 固定部分pip package版本号, 原库无版本, 项目代码老旧, 使得启动时各种报错代码.
* 其他: iteritem --> item 部分命令启用, 小小改动
* NEW: 放弃富文本编辑器WangEditor，改用Markdown编辑器Vditor

### Build

```shell
git clone https://github.com/Chopong/WeeklyReport_vditor && \
cd WeeklyReport_editor && \
docker build -t chopong/weeklyreport:vditor .
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
        -v db_name:weeklyreport \
        -v db_host:host.docker.internal \
        -v db_port:5432 \
        -v db_user:postgres \
        -v db_pass:postgres \
        chopong/weeklyreport:vditor
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
    image: chopong/weeklyreport:vditor
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
      - db_name=weeklyreport
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
    name: weekly
```



参考: 1. https://wr.mcloud.fun:81/auth/login

2. https://github.com/wuchaohua/WeeklyReport
3. https://github.com/CodingCrush/WeeklyReport

---

后台管理

第一次注册的用户为超级管理员，永远有登录后台的权限, 管理员可以修改其他角色


默认用户角色为`EMPLOYEE`(或`STUDENT`)，仅具有读写自己的周报的权限;

`MANAGER`可以读写周报，并查看本部门(学院)所有周报。

`HR`(或者`PROF`)可以读写周报，并查看全部门(学院)所有周报。

`ADMINISTRATOR`在`HR`(或`PROF`)基础上增加了进入后台的功能。

`QUIT`(或`ALUMNI`) 用来标识离职后的员工(或毕业的学生)，禁止其登录。
