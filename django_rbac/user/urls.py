from django.urls import path

from user.views import LoginView, TestView, CaptchaView, InfoView, SaveView, PwdView, ImageView, AvatarView, \
    SearchView, \
    ActionView, CheckUsernameView, CheckEmailView, CheckOtherEmailView, CheckOtherUsernameView, StatusView, \
    PasswordView, GrantRole

# from user.user_view import register, retrieve_password, send_register_code, send_retrieve_code, login

urlpatterns = [
    # admin
    path('login', LoginView.as_view(), name='login'),  # 登录
    path('info', InfoView.as_view(), name='info'),  # 查询用户信息
    path('save', SaveView.as_view(), name='save'),  # 添加或者修改用户信息
    path('uploadImage', ImageView.as_view(), name='uploadImage'),  # 头像上传
    path('updateAvatar', AvatarView.as_view(), name='updateAvatar'),  # 更新头像
    path('updateUserPwd', PwdView.as_view(), name='updateUserPwd'),  # 修改密码
    path('captcha', CaptchaView.as_view(), name='captcha'),  # 验证码
    path('search', SearchView.as_view(), name='search'),  # 用户信息查询
    path('action', ActionView.as_view(), name='action'),  # 用户信息操作
    path('checkUsername', CheckUsernameView.as_view(), name='checkUsername'),  # 用户名查重
    path('checkOtherUsername', CheckOtherUsernameView.as_view(), name='checkOtherUsername'),  # 用户名查重
    path('checkEmail', CheckEmailView.as_view(), name='checkEmail'),  # 邮箱查重
    # path('checkOtherEmail', CheckOtherEmailView.as_view(), name='checkOtherEmail'),  # 邮箱查重
    path('status', StatusView.as_view(), name='status'),  # 用户状态修改
    path('grantRole', GrantRole.as_view(), name='grant'),  # 角色授权
    path('resetPassword', PasswordView.as_view(), name='resetPassword'),  # 重置密码
    path('test', TestView.as_view(), name='test'),  # 测试
    # # user
    # path('userLogin', login, name='userLogin'),
    # path('send_register_code', send_register_code, name='send_register_code'),
    # path('send_retrieve_code', send_retrieve_code, name='send_retrieve_code'),
    # path('userRegister', register, name='userRegister'),  # 注册
    # path('reset_password', retrieve_password, name='retrieve_password'),  # 找回密码
]
