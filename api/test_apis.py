# coding=utf-8
"""
对views中的服务端api进行单元测试
"""
from django.test import TestCase, Client
from django.http import HttpResponse, JsonResponse, HttpRequest
from importlib import import_module
import api.views
import simplejson
import api.models
import doublegame.settings


class ModifySessionMixin(object):
    """
    支持test模拟session功能的基类
    """
    client = Client()

    def create_session(self):
        """
        为当前类创建模拟session功能
        """
        session_engine = import_module(doublegame.settings.SESSION_ENGINE)        
        store = session_engine.SessionStore()                          
        store.save()
        self.client.cookies[doublegame.settings.SESSION_COOKIE_NAME] = store.session_key


class GetCaptchaTestCase(TestCase):
    """
    对生成验证码函数进行测试,预期得到指定长度的验证码
    """

    def test_get_captcha_post_request(self):
        response = self.client.post('/api/captcha')
        self.assertEqual(response.status_code, 404)

    def test_get_captcha_get_request(self):
        response = self.client.get('/api/captcha')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        img = json['img']
        captcha = json['captcha']
        self.assertEqual(len(captcha), 4)


class RegisterTestCase(TestCase):
    """
    对注册功能进行测试,当用户发送的请求包含完整\规范的信息时,成功注册用户,返回'1',否则返回'0'
    """

    def test_register_get_request(self):
        response = self.client.get('/api/register')
        self.assertEqual(response.status_code, 404)

    def test_register_without_body(self):
        response = self.client.post('/api/register')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_register_success(self):
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'nickname': 'Tom',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/register', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')
        user = api.models.User.objects.get(email='tom@123.com')
        self.assertEqual(user.nickname, 'Tom')
        self.assertTrue(user.check_password('123456'))

    def test_register_with_wrong_email_format(self):
        data = {
            'email': 'aa@@tom.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'nickname': 'aa',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/register', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_register_without_captcha(self):
        data = {
            'email': 'aa@tom.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'nickname': 'aa'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/register', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_register_without_nickname(self):
        data = {
            'email': 'aa@tom.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/register', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_register_without_password(self):
        data = {
            'email': 'aa@tom.com',
            'nickname': 'aa',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/register', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_register_without_email(self):
        data = {
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'nickname': 'aa',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/register', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_register_with_wrong_crypted_password(self):
        data = {
            'email': 'aa@tom.com',
            'password': 'mXvXMG2g0YkE4GzyLVdg==',
            'nickname': 'aa',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/register', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_register_repeated_email(self):
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'nickname': 'Tom',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/register', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')
        response = self.client.post('/api/register', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')


class ResetPasswordEmailTestCase(TestCase):
    """
    对发送重置密码验证码功能进行测试,当用户发送的请求包含完整\规范的信息时,成功发送邮件,返回'1',否则返回'0'
    """

    def test_reset_password_email_get_request(self):
        response = self.client.get('/api/reset-password-email')
        self.assertEqual(response.status_code, 404)

    def test_reset_password_email_without_body(self):
        response = self.client.post('/api/reset-password-email')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_reset_password_email_success(self):
        api.models.User.objects.create_user(email='tom@qq.com', nickname='tom', password='123456')
        data = {'email': 'tom@qq.com'}
        data = simplejson.dumps(data)
        response = self.client.post('/api/reset-password-email', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')
        self.assertEqual(len(self.client.session['captcha']), 6)

    def test_reset_password_email_not_exist_user(self):
        data = {'email': '123@qwe.com'}
        data = simplejson.dumps(data)
        response = self.client.post('/api/reset-password-email', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')


class CheckEmailCaptchaTestCase(ModifySessionMixin, TestCase):
    """
    对检验验证码功能进行测试,当验证码正确时返回'1',否则返回'0'
    """

    def setUp(self):
        self.create_session()

    def test_check_email_captcha_post_method(self):
        response = self.client.post('/api/check-email-captcha')
        self.assertEqual(response.status_code, 404)

    def test_check_email_captcha_true(self):
        api.models.User.objects.create_user(email='tom@qq.com', nickname='tom', password='123456')
        data = {'email': 'tom@qq.com'}
        data = simplejson.dumps(data)
        response = self.client.post('/api/reset-password-email', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')
        self.assertEqual(len(self.client.session['captcha']), 6)
        captcha = self.client.session['captcha']
        response = self.client.get('/api/check-email-captcha?captcha='+ captcha)
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')

    def test_check_email_captcha_false(self):
        api.models.User.objects.create_user(email='tom@qq.com', nickname='tom', password='123456')
        data = {'email': 'tom@qq.com'}
        data = simplejson.dumps(data)
        response = self.client.post('/api/reset-password-email', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')
        self.assertEqual(len(self.client.session['captcha']), 6)
        captcha = self.client.session['captcha']
        response = self.client.get('/api/check-email-captcha?captcha='+ '000000')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_check_email_captcha_without_sesion(self):
        response = self.client.get('/api/check-email-captcha?captcha='+ '000000')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

class ResetPasswordTestCase(TestCase):
    """
    对重置密码功能进行测试,当用户发送的请求包含完整\规范的信息时,成功重置密码,返回'1',否则返回'0'
    """
    def test_reset_password_get_request(self):
        response = self.client.get('/api/reset-password')
        self.assertEqual(response.status_code, 404)

    def test_reset_password_without_body(self):
        response = self.client.post('/api/reset-password')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_reset_password_success(self):
        user = api.models.User.objects.create_user(email='tom@qwe.com', nickname='tom', password='111111')
        data = {
            'email': 'tom@qwe.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/reset-password', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')
        user = api.models.User.objects.get(email='tom@qwe.com')
        self.assertTrue(user.check_password('123456'))
    
    def test_reset_password_not_exist_user(self):
        data = {
            'email': 'tom@qwe.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/reset-password', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_reset_password_without_captcha(self):
        user = api.models.User.objects.create_user(email='tom@qwe.com', nickname='tom', password='111111')
        data = {
            'email': 'tom@qwe.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg=='
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/reset-password', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_reset_password_without_password(self):
        user = api.models.User.objects.create_user(email='tom@qwe.com', nickname='tom', password='111111')
        data = {
            'email': 'tom@qwe.com',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/reset-password', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_reset_password_without_email(self):
        user = api.models.User.objects.create_user(email='tom@qwe.com', nickname='tom', password='111111')
        data = {
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/reset-password', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_reset_password_with_wrong_crypted_password(self):
        user = api.models.User.objects.create_user(email='tom@qwe.com', nickname='tom', password='111111')
        data = {
            'email': 'tom@qwe.com',
            'password': 'mXvXMG2g0YkE4yLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/reset-password', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')


class CheckEmailTestCase(TestCase):
    """
    对邮箱查重功能进行测试,当用户检验的邮箱已经被注册时,返回'1',否则返回'0'
    """

    def setUp(self):
        user = api.models.User.objects.create_user(email='tom@qwe.com', nickname='tom', password='111111')

    def test_check_email_post_request(self):
        response = self.client.post('/api/check-email')
        self.assertEqual(response.status_code, 404)
    
    def test_check_email_used(self):
        response = self.client.get('/api/check-email?email=tom@qwe.com')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')

    def test_check_email_unused(self):
        response = self.client.get('/api/check-email?email=jerry@qwe.com')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_check_email_without_mail(self):
        response = self.client.get('/api/check-email')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')


class SaveMapTestCase(ModifySessionMixin, TestCase):
    """
    对保存地图功能进行测试,当用户发送的请求包含完整\规范的信息时,成功保存地图,返回'1',否则返回'0'
    """

    def setUp(self):
        self.create_session()
        api.models.User.objects.create_user(email='tom@123.com', nickname='tom', password='123456')
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')

    def test_save_map_get_method(self):
        response = self.client.get('/api/save-map')
        self.assertEqual(response.status_code, 404)

    def test_save_map_without_body(self):
        response = self.client.post('/api/save-map')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_save_map_success(self):
        map_str = '1000000000010000000010000000000000000000000000000000000000000000000000000000000000000000000000000000'
        data = {
            'mapString': map_str,
            'name': 'new map',
            'remarks': 'the remark'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/save-map', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')
        map_one = api.models.DesignedMaps.objects.all()[0]
        self.assertEqual(map_one.map, map_str)

    def test_save_map_without_map_string(self):
        data = {}
        data = simplejson.dumps(data)
        response = self.client.post('/api/save-map', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')


class ReadMapTestCase(ModifySessionMixin, TestCase):
    """
    对读取地图功能进行测试,当用户发送的请求包含完整\规范的信息时,成功读取地图,返回'1'和地图信息,否则返回'0'
    """

    def setUp(self):
        self.create_session()
        api.models.User.objects.create_user(email='tom@123.com', nickname='tom', password='123456')
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')

    def test_read_map_post_method(self):
        response = self.client.post('/api/read-map')
        self.assertEqual(response.status_code, 404)

    def test_get_map_success(self):
        map_str = '1000000000010000000010000000000000000000000000000000000000000000000000000000000000000000000000000000'
        data = {
            'mapString': map_str,
            'name': 'new map',
            'remarks': 'the remark'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/save-map', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')
        map_one = api.models.DesignedMaps.objects.all()[0]
        self.assertEqual(map_one.map, map_str)
        response = self.client.get(('/api/read-map?mapid=' + str(map_one.map_id)))
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')
        self.assertEqual(json['map'], map_str)

    def test_get_map_not_exist(self):
        response = self.client.get('/api/read-map?mapid=1')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')
    
    def test_get_map_without_map_id(self):
        response = self.client.get('/api/read-map')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')


class LoginTestCase(TestCase):
    """
    对登录功能进行测试,当用户发送的请求包含完整\规范\正确的信息或本地有cookie时,成功登录,返回'1',否则返回'0'
    """

    def setUp(self):
        user = api.models.User.objects.create_user(email='tom@123.com', nickname='Tom', password='123456')

    def test_login_other_method(self):
        response = self.client.delete('/api/login')
        self.assertEqual(response.status_code, 404)

    def test_login_post_without_body(self):
        response = self.client.post('/api/login')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_login_post_success(self):
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')

    def test_login_not_exist_user(self):
        data = {
            'email': 'jerry@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_login_not_without_email(self):
        data = {
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_login_not_without_password(self):
        data = {
            'email': 'tom@123.com',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_login_not_without_captcha(self):
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg=='
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_login_not_with_wrong_crypted_password(self):
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0Y4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_login_not_with_wrong_password(self):
        data = {
            'email': 'tom@123.com',
            'password': 'WTyloDf7UBkSNcmBeD3zvw==',
            'captcha': 'aaaa'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_login_get_without_session(self):
        response = self.client.get('/api/login')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_login_get_with_session(self):
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')
        response = self.client.get('/api/login')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')


class LogoutTestCase(TestCase):
    """
    对注销功能进行测试,成功注销返回'1',否则返回'0'
    """

    def setUp(self):
        user = api.models.User.objects.create_user(email='tom@123.com', nickname='Tom', password='123456')

    def test_logout_post_request(self):
        response = self.client.post('/api/logout')
        self.assertEqual(response.status_code, 404)
    
    def test_logout_success(self):
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')
        response = self.client.get('/api/logout')
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')

    def test_logout_without_session(self):
        response = self.client.get('/api/logout')
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')


class PayTestCase(ModifySessionMixin, TestCase):
    """
    对支付功能进行测试,成功弹窗返回'1'和url,否则返回'0'
    """

    def setUp(self):
        user = api.models.User.objects.create_user(email='tom@123.com', nickname='Tom', password='123456')
    
    def test_pauy_post_method(self):
        response = self.client.post('/api/pay')
        self.assertEqual(response.status_code, 404)
    
    def test_pay_get_success(self):
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')
        response = self.client.get('/api/pay')
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')
    
    def test_pay_without_session(self):
        response = self.client.get('/api/pay')
        self.assertEqual(response.status_code, 404)


class ReadLevelTestCase(TestCase):
    """
    对读取关卡功能进行测试,当用户发送的请求包含完整\规范的信息时,成功读取关卡,返回'1'和关卡信息,否则返回'0'
    """

    def setUp(self):
        api.models.GameLevels.objects.create(
            map_id=1,
            map='0000000000000000000000103000000010000000001000000000100000000010000000001040000000000000000000000000',
            tips='XXX误入了迷失森林，请根据它来时留下的小旗帮助它回家吧！',
            codes='go(3)',
            mode='[[0, 0], [0, 1], [0, 3], [0, 4], [0, 5], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [3, 0], [3, 1], [3, 2]]',
            name='XXX要回家'
        )
    
    def test_read_level_get_success(self):
        response = self.client.get('/api/read-level?mapid=1')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')
        self.assertEqual(json['map'], '0000000000000000000000103000000010000000001000000000100000000010000000001040000000000000000000000000')
        self.assertEqual(json['name'], 'XXX要回家')
        self.assertEqual(json['tips'], 'XXX误入了迷失森林，请根据它来时留下的小旗帮助它回家吧！')
        self.assertEqual(json['codes'], 'go(3)')
        self.assertEqual(json['mode'], '[[0, 0], [0, 1], [0, 3], [0, 4], [0, 5], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [3, 0], [3, 1], [3, 2]]')

    def test_read_level_not_exist(self):
        response = self.client.get('/api/read-level?mapid=2')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')


class ReadMapListTestCase(ModifySessionMixin, TestCase):
    """
    对读取关卡广场功能进行测试,当用户发送的请求包含完整\规范的信息时,成功读取关卡广场,返回'1'和关卡列表,否则返回'0'
    """

    def setUp(self):
        self.create_session()
        api.models.User.objects.create_user(email='tom@123.com', nickname='tom', password='123456')
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        map_str = '1000000000010000000010000000000000000000000000000000000000000000000000000000000000000000000000000000'
        data = {
            'mapString': map_str,
            'name': 'new map',
            'remarks': 'the remark'
        }
        data = simplejson.dumps(data)
        self.client.post('/api/save-map', data=data, content_type='application/json')

    def test_read_map_list_get_success(self):
        the_map = api.models.DesignedMaps.objects.all()[0]
        the_map.is_published = True
        the_map.save()
        self.create_session()
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        response = self.client.get('/api/read-map-list')
        self.assertEqual(response.status_code, 200)

    def test_read_map_list_without_maps(self):
        self.create_session()
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        response = self.client.get('/api/read-map-list')
        self.assertEqual(response.status_code, 200)


class ReadMyMapList(ModifySessionMixin, TestCase):
    """
    对读取我的关卡功能进行测试,当用户发送的请求包含完整\规范的信息时,成功读取我的关卡,返回'1'和关卡列表,否则返回'0'
    """

    def setUp(self):
        api.models.User.objects.create_user(email='tom@123.com', nickname='tom', password='123456')
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        map_str = '1000000000010000000010000000000000000000000000000000000000000000000000000000000000000000000000000000'
        data = {
            'mapString': map_str,
            'name': 'new map',
            'remarks': 'the remark'
        }
        data = simplejson.dumps(data)
        self.client.post('/api/save-map', data=data, content_type='application/json')

    def test_read_my_map_list_get_success(self):
        self.create_session()
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        response = self.client.get('/api/read-my-map-list')
        self.assertEqual(response.status_code, 200)
    
    def test_read_my_map_list_without_maps(self):
        the_map = api.models.DesignedMaps.objects.all()[0]
        the_map.delete()
        self.create_session()
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        response = self.client.get('/api/read-my-map-list')
        self.assertEqual(response.status_code, 200)

    
class ReadPublishedMapListTestCase(ModifySessionMixin, TestCase):
    """
    对读取我发布的地图功能进行测试,当用户发送的请求包含完整\规范的信息时,成功读取我发布的地图,返回'1'和关卡列表,否则返回'0'
    """

    def test_read_published_map_list(self):
        user = api.models.User.objects.create_user(email='tom@123.com', nickname='tom', password='123456')
        map_one = api.models.DesignedMaps.objects.create(
            map='111111',
            name='new map',
            remarks='none',
            author=user
        )
        self.create_session()
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        response = self.client.get('/api/read-published-map-list')
        self.assertEqual(response.status_code, 200)
        map_one.publish()
        response = self.client.post('/api/login', data=data, content_type='application/json')
        response = self.client.get('/api/read-published-map-list')
        self.assertEqual(response.status_code, 200)


class ReadFavoriteMapListTestCase(ModifySessionMixin, TestCase):
    """
    对读取收藏地图功能进行测试,当用户发送的请求包含完整\规范的信息时,成功读取收藏的地图,返回'1'和关卡列表,否则返回'0'
    """

    def test_read_favorite_map_list(self):
        author = api.models.User.objects.create_user(email='author@123.com', nickname='author', password='123456')
        player = api.models.User.objects.create_user(email='tom@123.com', nickname='player', password='123456')
        map_one = api.models.DesignedMaps.objects.create(
            map='111111',
            name='new map',
            remarks='none',
            author=author
        )
        favor = api.models.FavoriteMaps.objects.create(user=player, map=map_one)
        self.create_session()
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        response = self.client.get('/api/read-favorite-map-list')
        self.assertEqual(response.status_code, 200)
        favor.delete()
        response = self.client.get('/api/read-favorite-map-list')
        self.assertEqual(response.status_code, 200)


class ChangePublishStatus(ModifySessionMixin, TestCase):
    """
    对修改发布状态功能进行测试,当用户发送的请求包含完整\规范的信息时,成功修改发布状态,返回'1',否则返回'0'
    """
    def test_change_publish_status(self):
        user = api.models.User.objects.create_user('tom@123.com', 'tom', '123456')
        the_map = api.models.DesignedMaps.objects.create(
            map='111111',
            name='1',
            remarks='2',
            author=user
        )
        self.create_session()
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        data = {
            'mapid': the_map.map_id,
            'status': 1
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/change-publish', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        maps = api.models.DesignedMaps.objects.filter(is_published=True)
        self.assertEqual(len(maps), 1)
        data = {
            'mapid': the_map.map_id,
            'status': 0
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/change-publish', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        maps = api.models.DesignedMaps.objects.filter(is_published=True)
        self.assertEqual(len(maps), 0)


class DeleteMapTestCase(ModifySessionMixin, TestCase):
    """
    对删除地图功能进行测试,当用户发送的请求包含完整\规范的信息时,成功删除地图,返回'1',否则返回'0'
    """
    def test_delete_map(self):
        user = api.models.User.objects.create_user('tom@123.com', 'tom', '123456')
        the_map = api.models.DesignedMaps.objects.create(
            map='111111',
            name='1',
            remarks='2',
            author=user
        )
        self.create_session()
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        data = {
            'mapid': the_map.map_id
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/delete-map', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        maps = api.models.DesignedMaps.objects.all()
        self.assertEqual(len(maps), 0)


class ChangeNicknameTestCase(ModifySessionMixin, TestCase):
    """
    对修改昵称功能进行测试,当用户发送的请求包含完整\规范的信息时,成功修改昵称,返回'1',否则返回'0'
    """
    def test_change_nickname(self):
        user = api.models.User.objects.create_user('tom@123.com', 'tom', '123456')
        self.create_session()
        data = {
            'email': 'tom@123.com',
            'password': 'mXvXMG2g0YkE4GzyLVn/dg==',
            'captcha': 'abcd'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/login', data=data, content_type='application/json')
        data = {
            'nickname': 'jerry'
        }
        data = simplejson.dumps(data)
        response = self.client.post('/api/change-nickname', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        user = api.models.User.objects.all()[0]
        self.assertEqual(user.nickname, 'jerry')
