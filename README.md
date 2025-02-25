# Django-Vue-RBAC 后台管理系统
基于Django5.1和Python3.10的rbac系统
## 主要功能
- 后台验证码登录
![image](https://github.com/leleleocc/django-vue-rbac/tree/master/pictures/login.png)
- 基本的用户管理、角色管理、菜单管理
- 用户管理(包括用户的增删查改以及角色的分配)
![image](https://github.com/leleleocc/django-vue-rbac/tree/master/pictures/user.png)
- 角色管理(包括角色的增删查改以及权限的分配)
![image](https://github.com/leleleocc/django-vue-rbac/tree/master/pictures/role.png)
- 菜单管理(包括权限路由的增删查改以及权限的分配)
![image](https://github.com/leleleocc/django-vue-rbac/tree/master/pictures/menu.png)
## 使用教程
- 使用前配置setting.py中的database和redis
- 启用Mysql服务，redis-server启动redis
- 运行数据库迁移命令
```python
python manage.py makemigrations
python manage.py migrate
```
- 向数据库插入测试数据，实例sql如下
```sql
insert into `sys_user`(`id`, `username`, `password`, `avatar`, `email`, `phonenumber`, `login_date`, `status`, `create_time`, `update_time`, `remark`) 
values(1,'admin','e10adc3949ba59abbe56e057f20f883e','default.jpg','admin@163.com','17621935888','2025-02-25 14:30:00','1','2025-02-25 14:30:00','2025-02-25 14:30:00','超级管理员');
insert  into `sys_role`(`id`,`name`,`code`,`create_time`,`update_time`,`remark`) values 
(1,'超级管理员','admin','2025-02-25 14:30:00','2025-02-25 14:30:00','拥有系统最高权限');
insert  into `sys_menu`(`id`,`name`,`icon`,`parent_id`,`order_num`,`path`,`component`,`menu_type`,`perms`,`create_time`,`update_time`,`remark`) values 
(1,'系统管理','system',0,1,'/sys','','M','','2025-02-25 14:30:00','2025-02-25 14:30:00','系统管理目录'),
(2,'用户管理','user',1,1,'/sys/user','sys/user/index','C','system:user:list','2025-02-25 14:30:00','2025-02-25 14:30:00','用户管理菜单'),
(3,'角色管理','peoples',1,2,'/sys/role','sys/role/index','C','system:role:list','2025-02-25 14:30:00','2025-02-25 14:30:00','角色管理菜单'),
(4,'菜单管理','tree-table',1,3,'/sys/menu','sys/menu/index','C','system:menu:list','2025-02-25 14:30:00','2025-02-25 14:30:00','菜单管理菜单');
insert  into `sys_role_menu`(`id`,`menu_id`,`role_id`) values 
(1,1,1),(2,2,1),(3,3,1),(4,4,1);
insert  into `sys_user_role`(`id`,`role_id`,`user_id`) values 
(1,1,1);
```
- 查看ip地址，将vue-rbac/src/utils/request.js中的baseUrl修改为本地的ip:port
- `python manage.py runserver ip:port`启动django,ip和port换成本地的
- `npm run server`启动vue，通过本地ip:8080访问后台，登录时使用已经插入的数据(username:admin,password:123456)
