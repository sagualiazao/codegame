# coding=utf-8
from django.test import TestCase
from django.http import HttpResponse, JsonResponse, HttpRequest
import api.views
import simplejson
import api.models


class GetCaptchaTestCase(TestCase):

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
        self.assertEqual(len(json['captcha']), 6)

    def test_reset_password_email_not_exist_user(self):
        data = {'email': '123@qwe.com'}
        data = simplejson.dumps(data)
        response = self.client.post('/api/reset-password-email', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')


class ResetPasswordTestCase(TestCase):

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


class SaveMapTestCase(TestCase):

    def test_save_map_get_method(self):
        response = self.client.get('/api/save-map')
        self.assertEqual(response.status_code, 404)

    def test_save_map_without_body(self):
        response = self.client.post('/api/save-map')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')

    def test_save_map_success(self):
        data = {'mapString': '111111'}
        data = simplejson.dumps(data)
        response = self.client.post('/api/save-map', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')
        map_one = api.models.GameLevels.objects.all()[0]
        self.assertEqual(map_one.map, '111111')

    def test_save_map_without_map_string(self):
        data = {}
        data = simplejson.dumps(data)
        response = self.client.post('/api/save-map', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '0')


class ReadMapTestCase(TestCase):
    
    def test_read_map_post_method(self):
        response = self.client.post('/api/read-map')
        self.assertEqual(response.status_code, 404)

    def test_get_map_success(self):
        data = {'mapString': '111111'}
        data = simplejson.dumps(data)
        response = self.client.post('/api/save-map', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')
        map_one = api.models.GameLevels.objects.all()[0]
        response = self.client.get(('/api/read-map?mapid=' + str(map_one.map_id)))
        self.assertEqual(response.status_code, 200)
        json = simplejson.loads(response.content)
        self.assertEqual(json['status'], '1')
        self.assertEqual(json['map'], '111111')

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
