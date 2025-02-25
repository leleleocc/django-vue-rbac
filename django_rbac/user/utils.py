import jwt
from datetime import datetime, timedelta
from .models import SysRole, SysMenu  # 引入 UserRole 模型
from rest_framework.authentication import BaseAuthentication
from django.core.cache import cache  # 导入缓存模块
from random import Random
from django.core.mail import send_mail
from django.conf import settings


class JWTAuthentication(BaseAuthentication):
    @staticmethod
    def generate_access_token(user):
        """生成 JWT token，添加角色信息"""
        # 获取用户的角色信息
        # roleList = SysRole.objects.raw(
        #     "select id,name from sys_role where id in (select role_id from sys_user_role where user_id=" + str(
        #         user.id) + ")")
        # roles = ",".join([role.name for role in roleList])
        payload = {
            'user_id': user.id,
            # 'roles': roles,  # 在 payload 中添加角色信息
            'exp': datetime.utcnow() + timedelta(hours=1),  # 设置 token 过期时间为 1 小时
            'iat': datetime.utcnow()  # 签发时间
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    # @staticmethod
    # def unavailable_url(user_id):
    #     roleList = SysRole.objects.raw(
    #         "select id,name from sys_role where id in (select role_id from sys_user_role where user_id=" + str(
    #             user_id) + ")")
    #     role_ids = [role.id for role in roleList]
    #     menuSet = set()
    #     for role_id in role_ids:
    #         menuList = SysMenu.objects.raw(
    #             "select * from sys_menu where id in (select menu_id from sys_role_menu where role_id=" + str(
    #                 role_id) + ")")
    #         for menu in menuList:
    #             menuSet.add(menu.path)
    #     menuAll = SysMenu.objects.all()
    #     menuSetAll = set([menu.path for menu in menuAll])
    #     menu_not_allow = menuSetAll - menuSet
    #     # print("menuSetAll", menuSetAll, '\n', 'menuSet', menuSet)
    #     print("menu_not_allow", menu_not_allow)
    #     return menu_not_allow


class CommonJsonResponse:
    @staticmethod
    def success(data=None, msg="操作成功", code=200):
        return {
            "code": code,
            "msg": msg,
            "data": data
        }

    @staticmethod
    def fail(data=None, msg="操作失败", code=500):
        return {
            "code": code,
            "msg": msg,
            "data": data
        }

    @staticmethod
    def reload(data=None, msg="请重新登录", code=401):
        return {
            "code": code,
            "msg": msg,
            "data": data
        }

    @staticmethod
    def wrong_permission(data=None, msg="没有权限", code=400):
        return {
            "code": code,
            "msg": msg,
            "data": data
        }
