import base64
import copy
import hashlib
import json
import os
import random
import uuid
from datetime import datetime, timedelta
from io import BytesIO

import jwt
from captcha.image import ImageCaptcha
from django.core import serializers
from django.core.cache import cache
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.http import JsonResponse, QueryDict
from django.views import View
from user.utils import JWTAuthentication

from django_rbac import settings
from user.models import SysUser, SysUserSerializer, SysRole, SysMenu, SysMenuSerializer, SysUserRole


# Create your views here.
class LoginView(View):

    # 构造菜单树
    def buildTreeMenu(self, sysMenuList):
        resultMenuList: list[SysMenu] = list()
        for menu in sysMenuList:
            # 寻找子节点
            for e in sysMenuList:
                if e.parent_id == menu.id:
                    if not hasattr(menu, "children"):
                        menu.children = list()
                    menu.children.append(e)
            # 判断父节点，添加到集合
            if menu.parent_id == 0:
                resultMenuList.append(menu)
        return resultMenuList

    def post(self, request):
        # data = json.loads(request.body.decode("utf-8"))
        username = request.GET.get('username')
        password = request.GET.get('password')
        code = request.GET.get('code')  # 用户填写的验证码
        uuid = request.GET.get('uuid')
        token = ''
        # print(password, hashlib.md5(password.encode()).hexdigest())
        captcha = cache.get(uuid)
        print("captcha", captcha)
        if captcha == '' or captcha.lower() != code.lower():  # 判断验证码
            return JsonResponse({'code': 500, 'info': '验证码错误！'})
        try:
            user = SysUser.objects.get(username=username, password=hashlib.md5(password.encode()).hexdigest())
            token = JWTAuthentication.generate_access_token(user)
            redis_key = f"user_{user.id}_token"
            cache.set(redis_key, token, timeout=60 * 60 * 12)  # 设置 token 过期时间为 12 小时
            print("登录token:", token, "\nredis_key", redis_key)
            # roleList = SysRole.objects.raw("select id,role_id from sys_user_role where user_id=" + str(user.id))
            # 获取该用户的角色
            roleList = SysRole.objects.raw(
                "select id,name from sys_role where id in (select role_id from sys_user_role where user_id=" + str(
                    user.id) + ")")
            menuSet: set[SysMenu] = set()  # 存放该用户可访问的所有菜单（路由）
            # roles:str = ""  # 当前用户拥有的角色，逗号隔开
            roles = ",".join([role.name for role in roleList])
            for row in roleList:
                menuList = SysMenu.objects.raw(
                    "select * from sys_menu where id in (select menu_id from sys_role_menu where role_id=" + str(
                        row.id) + ")")
                for row2 in menuList:
                    menuSet.add(row2)
            menuList: list[SysMenu] = list(menuSet)  # set转list
            # print(menuList)
            sorted_menuList = sorted(menuList)  # 根据order_num排序
            # 构造菜单树
            sysMenuList: list[SysMenu] = self.buildTreeMenu(sorted_menuList)
            # print(sysMenuList)
            serializerMenuList: list[SysMenuSerializer] = list()
            for sysMenu in sysMenuList:
                serializerMenuList.append(SysMenuSerializer(sysMenu).data)

        except Exception as e:
            print(e)
            return JsonResponse({'code': 500, 'info': '用户名或者密码错误！'})
        return JsonResponse(
            {'code': 200, 'user': SysUserSerializer(user).data, 'token': token, 'roles': roles,
             'menuList': serializerMenuList})


class InfoView(View):

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        print("result=", payload)


# 用户角色授权
class GrantRole(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        user_id = data['id']
        roleIdList = data['roleIds']
        print(user_id, roleIdList)
        SysUserRole.objects.filter(user_id=user_id).delete()  # 删除用户角色关联表中的指定用户数据
        for roleId in roleIdList:
            userRole = SysUserRole(user_id=user_id, role_id=roleId)
            userRole.save()
        return JsonResponse({'code': 200})


# 修改密码
class PwdView(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        id = data['id']
        oldPassword = data['oldPassword']
        newPassword = data['newPassword']
        obj_user = SysUser.objects.get(id=id)
        if obj_user.password == hashlib.md5(oldPassword.encode()).hexdigest():
            obj_user.password = hashlib.md5(newPassword.encode()).hexdigest()
            # obj_user.update_time = datetime.now().date()
            obj_user.save()
            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'code': 500, 'errorInfo': '原密码错误！'})


# 添加/修改信息
class SaveView(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        print("data:", data)
        if data['id'] == -1:  # 添加
            obj_sysUser = SysUser(username=data['username'], password=data['password'],
                                  email=data['email'], phonenumber=data['phonenumber'],
                                  status=data['status'],
                                  remark=data['remark'])
            # obj_sysUser.create_time = datetime.now().date()
            obj_sysUser.avatar = 'default.jpg'
            obj_sysUser.password = hashlib.md5("123456".encode()).hexdigest()
            obj_sysUser.save()
        else:  # 修改
            obj_sysUser = SysUser(id=data['id'], username=data['username'], password=data['password'],
                                  avatar=data['avatar'], email=data['email'], phonenumber=data['phonenumber'],
                                  login_date=data['login_date'], status=data['status'], remark=data['remark'])
            # obj_sysUser.update_time = datetime.now().date()
            obj_sysUser.save()
        return JsonResponse({'code': 200})


# 用户状态修改
class StatusView(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        id = data['id']
        status = data['status']
        user_object = SysUser.objects.get(id=id)
        user_object.status = status
        user_object.save()
        return JsonResponse({'code': 200})


# 重置密码
class PasswordView(View):

    def get(self, request):
        id = request.GET.get("id")
        user_object = SysUser.objects.get(id=id)
        user_object.password = hashlib.md5("123456".encode()).hexdigest()
        # user_object.update_time = datetime.now().date()
        user_object.save()
        return JsonResponse({'code': 200})


class TestView(View):

    def post(self, request):
        return JsonResponse({'code': 200, 'info': '测试！'})


# 用户名查重
class CheckUsernameView(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        username = data['username']
        # print("username=", username)
        if SysUser.objects.filter(username=username).exists():
            return JsonResponse({'code': 500})
        else:
            return JsonResponse({'code': 200})


class CheckOtherUsernameView(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        username = data['username']
        id_ = data['id']
        print("username=", username)
        print("id=", id_)
        if SysUser.objects.filter(username=username).exclude(id=id_).exists():
            return JsonResponse({'code': 500})
        else:
            return JsonResponse({'code': 200})


# 邮箱查重
class CheckEmailView(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        email = data['email']
        # print("email=", email)
        if SysUser.objects.filter(email=email).exists():
            return JsonResponse({'code': 500})
        else:
            return JsonResponse({'code': 200})


class CheckOtherEmailView(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        email = data['email']
        id_ = data['id']
        if SysUser.objects.filter(email=email).exclude(id=id_).exists():
            return JsonResponse({'code': 500})
        else:
            return JsonResponse({'code': 200})


# 用户基本操作
class ActionView(View):

    def get(self, request):
        """
        根据id获取用户信息
        :param request:
        :return:
        """
        id = request.GET.get("id")
        user_object = SysUser.objects.get(id=id)
        return JsonResponse({'code': 200, 'user': SysUserSerializer(user_object).data})

    def delete(self, request):
        """
        删除操作
        :param request:
        :return:
        """
        idList = json.loads(request.body.decode("utf-8"))
        SysUserRole.objects.filter(user_id__in=idList).delete()
        SysUser.objects.filter(id__in=idList).delete()
        return JsonResponse({'code': 200})


# 用户信息查询
class SearchView(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        pageNum = data['pageNum']  # 当前页
        pageSize = data['pageSize']  # 每页大小
        query = data['query']  # 查询参数
        # print(pageSize, pageNum)
        userListPage = Paginator(SysUser.objects.filter(username__icontains=query).order_by('id'), pageSize).page(
            pageNum)
        obj_users = userListPage.object_list.values()  # 转成字典
        users = list(obj_users)  # 把外层的容器转为List
        for user in users:
            userId = user['id']
            # roleList = SysRole.objects.raw("select id,user_id,role_id from sys_user_role where user_id=" + str(userId))
            roleList = SysRole.objects.raw(
                "select id,name from sys_role where id in (select role_id from sys_user_role where user_id=" + str(
                    userId) + ")")
            roles = ",".join([role.name for role in roleList])
            roleListDict = []
            for role in roleList:
                roleDict = {}
                roleDict['id'] = role.id
                roleDict['name'] = role.name
                roleListDict.append(roleDict)

            user['roleList'] = roleListDict
        total = SysUser.objects.filter(username__icontains=query).count()
        # print(user)
        return JsonResponse(
            {'code': 200, 'userList': users, 'total': total})


class AvatarView(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        id = data['id']
        avatar = data['avatar']
        obj_user = SysUser.objects.get(id=id)
        obj_user.avatar = avatar
        obj_user.save()
        return JsonResponse({'code': 200})


class ImageView(View):

    def post(self, request):
        file = request.FILES.get('avatar')
        # print("file:", file)
        if file:
            file_name = file.name
            suffixName = file_name[file_name.rfind("."):]
            new_file_name = datetime.now().strftime('%Y%m%d%H%M%S') + suffixName
            file_path = str(settings.MEDIA_ROOT) + "\\userAvatar\\" + new_file_name
            print("file_path:", file_path)
            try:
                with open(file_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                return JsonResponse({'code': 200, 'title': new_file_name})
            except:
                return JsonResponse({'code': 500, 'errorInfo': '上传头像失败'})


class CaptchaView(View):

    def get(self, request):
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        data = ''.join(random.sample(characters, 4))
        print("data", data)
        captcha = ImageCaptcha()
        imageData: BytesIO = captcha.generate(data)
        base64_str = base64.b64encode(imageData.getvalue()).decode()
        # print(type(base64_str), base64_str)
        random_uuid = uuid.uuid4()  # 生成一个随机数
        # print(random_uuid)
        cache.set(random_uuid, data, timeout=300)  # 存到redis缓存中 有效期5分钟
        return JsonResponse({'code': 200, 'base64str': 'data:image/png;base64,' + base64_str, 'uuid': random_uuid})
