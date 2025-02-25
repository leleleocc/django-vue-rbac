from django.utils.deprecation import MiddlewareMixin
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError
import jwt
from django.conf import settings
from user.utils import JWTAuthentication
from user.utils import CommonJsonResponse
from django.core.cache import cache


class JwtAuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        white_list = ["/user/login", "/user/captcha"]
        path = request.path
        if path not in white_list and not path.startswith("/media"):
            print(path, '要验证')
            token = request.META.get('HTTP_AUTHORIZATION')
            print("token", token)
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('user_id')
                redis_key = f"user_{user_id}_token"
                stored_token = cache.get(redis_key)
                cache.set(redis_key, stored_token, timeout=60 * 60 * 12)  # 每次访问都重设过期时间为  12小时
                if token != stored_token:
                    return CommonJsonResponse.reload('Token 无效，请重新登录！')
                # menu_not_allow = JWTAuthentication.unavailable_url(user_id)
                # if request.path in menu_not_allow:
                #     return CommonJsonResponse.wrong_permission('没有权限访问！')
            except ExpiredSignatureError:
                print("Token过期")
                return CommonJsonResponse.reload('Token过期，请重新登录！')
            except InvalidTokenError:
                print("Token无效")
                return CommonJsonResponse.reload('Token验证失败！')
            except PyJWTError:
                print("Token验证异常！")
                return CommonJsonResponse.reload('Token验证异常！')
        else:
            print("不需要验证")
            return None
