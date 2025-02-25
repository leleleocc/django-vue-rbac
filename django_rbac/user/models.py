from django.db import models
from rest_framework import serializers


# Create your models here.
# 系统用户类
class SysUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=100, verbose_name="密码")
    avatar = models.CharField(max_length=255, null=True, verbose_name="用户头像")
    email = models.CharField(max_length=100, unique=True, verbose_name="用户邮箱")
    phonenumber = models.CharField(max_length=11, null=True, verbose_name="手机号码")
    login_date = models.DateTimeField(null=True, verbose_name="最后登录时间")
    status = models.IntegerField(null=True, verbose_name="帐号状态（0正常 1停用）")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    remark = models.CharField(max_length=500, null=True, verbose_name="备注")

    class Meta:
        db_table = "sys_user"


class SysUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysUser
        fields = '__all__'


class SysMenu(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, verbose_name="菜单名称")
    icon = models.CharField(max_length=100, null=True, verbose_name="菜单图标")
    parent_id = models.IntegerField(null=True, verbose_name="父菜单ID")
    order_num = models.IntegerField(null=True, verbose_name="显示顺序")
    path = models.CharField(max_length=200, null=True, verbose_name="路由地址")
    component = models.CharField(max_length=255, null=True, verbose_name="组件路径")
    menu_type = models.CharField(max_length=1, null=True, verbose_name="菜单类型（M目录 C菜单 F按钮）")
    perms = models.CharField(max_length=100, null=True, verbose_name="权限标识")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    remark = models.CharField(max_length=500, null=True, verbose_name="备注")

    # children = list()

    def __lt__(self, other):
        return self.order_num < other.order_num

    class Meta:
        db_table = "sys_menu"


class SysMenuSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    # 只使用于二级目录
    def get_children(self, obj):
        print("子菜单序列化")
        if hasattr(obj, "children"):
            serializerMenuList: list[SysMenuSerializer2] = list()
            for sysMenu in obj.children:
                serializerMenuList.append(SysMenuSerializer2(sysMenu).data)
            return serializerMenuList

    class Meta:
        model = SysMenu
        fields = '__all__'


class SysMenuSerializer2(serializers.ModelSerializer):
    class Meta:
        model = SysMenu
        fields = '__all__'


# 系统角色类
class SysRole(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=True, verbose_name="角色名称")
    code = models.CharField(max_length=100, null=True, verbose_name="角色权限字符串")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    remark = models.CharField(max_length=500, null=True, verbose_name="备注")

    class Meta:
        db_table = "sys_role"


class SysRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysRole
        fields = '__all__'


# 系统角色菜单关联类
class SysRoleMenu(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(SysRole, on_delete=models.PROTECT)
    menu = models.ForeignKey(SysMenu, on_delete=models.PROTECT)

    class Meta:
        db_table = "sys_role_menu"


class SysRoleMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysRoleMenu
        fields = '__all__'


# 系统用户角色关联类
class SysUserRole(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(SysRole, on_delete=models.PROTECT)
    user = models.ForeignKey(SysUser, on_delete=models.PROTECT)

    class Meta:
        db_table = "sys_user_role"


class SysUserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysUserRole
        fields = '__amll__'
