# coding=utf-8
import unittest
import api.utils
import re
from django.test import TestCase, Client
import simplejson


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


class CaptchaTestCase(unittest.TestCase):

    def test_captcha_default_length(self):
        captcha_str = api.utils.Captcha.string_captcha()
        img, captcha_img = api.utils.Captcha.generate_captcha()
        self.assertEqual(len(captcha_str), 6)
        self.assertEqual(len(captcha_img), 4)

    def test_captcha_character_set(self):
        captcha = api.utils.Captcha.string_captcha()
        self.assertTrue(re.match(r'[a-zA-NP-Z0-9]{6}', captcha))

    def test_captcha_can_set_length(self):
        captcha = api.utils.Captcha.string_captcha(10)
        self.assertEqual(len(captcha), 10)


class CbcTestCase(unittest.TestCase):

    def test_cbc_raise_typeerror_if_not_str(self):
        key_str = 123
        data = '这是一句话'
        api.utils.CBC.crypt('key', 'data')
        with self.assertRaises(TypeError):
            api.utils.CBC.crypt(key_str, data)
        with self.assertRaises(TypeError):
            api.utils.CBC.decrypt(key_str, data)

    def test_cbc_can_crypt_correctly(self):
        key_str = 'abcd'
        data = '这是一句话。'
        crypted_data = api.utils.CBC.crypt(key_str=key_str, data=data)
        decrypted_data = api.utils.CBC.decrypt(key_str=key_str, data=crypted_data)
        self.assertEqual(decrypted_data, data)

class CheckEmailFormatTestCase(unittest.TestCase):

    def test_check_email_fromat(self):
        email_one = 'abc@zxc.com'
        email_two = 'a_b_c@qwe.com'
        email_three = 'abc@qwe.aqwe.com.cn'
        email_four = 'a@s@qq.com'
        email_five = '@asd.com.cn'
        email_six = '啊@qwe.com'
        email_seven = 'qwert'
        email_eight = 'qwer.com'
        email_nine = 'qwer@qwer.'
        email_ten = 'qwe@qwe..com'
        self.assertTrue(api.utils.check_email_format(email_one))
        self.assertTrue(api.utils.check_email_format(email_two))
        self.assertTrue(api.utils.check_email_format(email_three))
        self.assertFalse(api.utils.check_email_format(email_four))
        self.assertFalse(api.utils.check_email_format(email_five))
        self.assertFalse(api.utils.check_email_format(email_six))
        self.assertFalse(api.utils.check_email_format(email_seven))
        self.assertFalse(api.utils.check_email_format(email_eight))
        self.assertFalse(api.utils.check_email_format(email_nine))
        self.assertFalse(api.utils.check_email_format(email_ten))

class SimpleResponseTest(ModifySessionMixin, TestCase):

    def test_blank_func(self):
        api.utils.blank_func()
        self.assertTrue(True)

    def test_user_json_response(self):
        tom = api.models.User.objects.create_user('tom@123.com', 'tom', '123456')
        json = api.utils.SimpleResponse.user_json_response(tom)
        json = simplejson.loads(json.content)
        self.assertEqual(json['status'], '1')
        self.assertEqual(json['email'], 'tom@123.com')
    
    def test_designed_map_json_response(self):
        tom = api.models.User.objects.create_user('tom@123.com', 'tom', '123456')
        the_map = api.models.DesignedMaps.objects.create(
            map='123456',
            name='1',
            remarks='2',
            author=tom
        )
        json = api.utils.SimpleResponse.designed_map_json_response(the_map)
        json = simplejson.loads(json.content)
        self.assertEqual(json['status'], '1')
        self.assertEqual(json['author'], 'tom@123.com')

    def test_game_level_json_response(self):
        level = api.models.GameLevels.objects.create(
            map_id=1,
            map='123456',
            name='1',
            tips='2',
            codes='3',
            mode='4'
        )
        json = api.utils.SimpleResponse.game_level_json_response(level)
        json = simplejson.loads(json.content)
        self.assertEqual(json['status'], '1')
        self.assertEqual(json['map'], '123456')
    