# coding=utf-8
"""
对数据模型进行单元测试的测试文件
"""
from django.test import TestCase
from api.models import User, GameLevels, DesignedMaps, FavoriteMaps


class UserTestCase(TestCase):
    """
    测试User模型
    """
    def setUp(self):
        User.objects.create_user(email='tom@123.com', password='123456', nickname='Tom')
        User.objects.create_user(email='jerry@123.com', password='就是汉字密码', nickname='杰瑞')

    def test_user_can_be_created(self):
        """
        测试user对象是否能正确被创建
        """
        tom = User.objects.filter(email='tom@123.com')
        jerry = User.objects.filter(email='jerry@123.com')
        self.assertEqual(len(tom), 1)
        self.assertEqual(len(jerry), 1)
        self.assertTrue(tom[0].check_password('123456'))
        self.assertTrue(jerry[0].check_password('就是汉字密码'))
        self.assertEqual(tom[0].nickname, 'Tom')
        self.assertEqual(jerry[0].nickname, '杰瑞')

    def test_user_get_name(self):
        """
        测试继承的get_full_name()和get_short_name()函数是否能正确工作
        """
        tom = User.objects.filter(email='tom@123.com')
        self.assertEqual(tom[0].get_full_name(), 'tom@123.com')
        self.assertEqual(tom[0].get_short_name(), 'tom@123.com')

    def test_create_user_without_email(self):
        """
        测试创建没有email字段的用户是否抛出异常
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(email=False, password='123456', nickname='Tom')

    def test_user_default_values(self):
        """
        测试user用户的默认值
        """
        tom = User.objects.get(email='tom@123.com')
        jerry = User.objects.get(email='jerry@123.com')
        self.assertFalse(tom.has_paied)
        self.assertFalse(jerry.has_paied)
        self.assertEqual(tom.game_progress, 0)
        self.assertEqual(jerry.game_progress, 0)

    def test_user_reset_password(self):
        """
        测试user用户修改密码操作
        """
        tom = User.objects.get(email='tom@123.com')
        jerry = User.objects.get(email='jerry@123.com')
        tom.set_password('654321')
        jerry.set_password('新的汉字密码')
        self.assertTrue(tom.check_password('654321'))
        self.assertTrue(jerry.check_password('新的汉字密码'))


class GameLevelsTestCase(TestCase):
    """
    测试GameLevels模型
    """
    def setUp(self):
        GameLevels.objects.create(
            map='111111',
            level_three_steps=10,
            level_two_steps=20,
            tips='This is a tip',
            goal='This is a goal'
        )
        GameLevels.objects.create(
            map='222222',
            level_three_steps=10,
            level_two_steps=20,
            tips='这是汉字提示',
            goal='这是汉字目标'
        )

    def test_game_level_can_be_created(self):
        """
        测试GameLevels对象是否能被正确创建
        """
        level_one = GameLevels.objects.get(map_id=1)
        level_two = GameLevels.objects.get(map_id=2)
        self.assertEqual(level_one.map, '111111')
        self.assertEqual(level_two.map, '222222')
        self.assertEqual(level_one.level_three_steps, 10)
        self.assertEqual(level_two.level_three_steps, 10)
        self.assertEqual(level_one.level_two_steps, 20)
        self.assertEqual(level_two.level_two_steps, 20)
        self.assertEqual(level_one.tips, 'This is a tip')
        self.assertEqual(level_two.tips, '这是汉字提示')
        self.assertEqual(level_one.goal, 'This is a goal')
        self.assertEqual(level_two.goal, '这是汉字目标')


class DesignedMapsTestCase(TestCase):
    """
    测试DesignedMaps对象
    """
    def setUp(self):
        author = User.objects.create_user(email='author@123.com', nickname='author', password='123456')
        DesignedMaps.objects.create(
            map='111111',
            name='new map',
            remarks='none',
            author=author
        )

    def test_designed_maps_can_be_created(self):
        """
        测试DesignedMaps对象是否能被正确创建
        """
        author = User.objects.get(email='author@123.com')
        map_one = DesignedMaps.objects.get(map_id=1)
        self.assertEqual(map_one.map, '111111')
        self.assertEqual(map_one.name, 'new map')
        self.assertEqual(map_one.remarks, 'none')
        self.assertEqual(map_one.author, author)
        self.assertFalse(map_one.is_published)

    def test_designed_maps_can_be_published(self):
        """
        测试DesignedMaps对象使用publish()函数是否正常
        """
        map_one = DesignedMaps.objects.all()[0]
        map_one.publish()
        map_one = DesignedMaps.objects.all()[0]
        self.assertTrue(map_one.is_published)

    def test_designed_maps_can_cancel_publish(self):
        """
        测试DesignedMaps对象使用cancel_publish()函数是否正常
        """
        map_one = DesignedMaps.objects.all()[0]
        map_one.is_published = True
        map_one.save()
        map_one.cancel_publish()
        self.assertFalse(map_one.is_published)

    def test_designed_maps_can_be_deleted(self):
        """
        测试DesignedMaps对象被删除是否正常
        """
        map_one = DesignedMaps.objects.all()[0]
        map_one.delete()
        map_one = DesignedMaps.objects.all()
        self.assertEqual(len(map_one), 0)


class FavoriteMapsTestCase(TestCase):
    """
        测试FavoriteMaps对象
    """
    def setUp(self):
        author = User.objects.create_user(email='author@123.com', nickname='author', password='123456')
        player = User.objects.create_user(email='player@123.com', nickname='player', password='123456')
        map_one = DesignedMaps.objects.create(
            map='111111',
            name='new map',
            remarks='none',
            author=author
        )
        FavoriteMaps.objects.create(user=player, map=map_one)

    def test_favorite_maps_can_be_created(self):
        """
        测试FavoriteMaps对象是否能正确被创建
        """
        favorite = FavoriteMaps.objects.all()[0]
        player = User.objects.get(email='player@123.com')
        map_one = DesignedMaps.objects.all()[0]
        self.assertEqual(favorite.user, player)
        self.assertEqual(favorite.map, map_one)

    def test_favorite_maps_can_be_deleted(self):
        """
        测试DesignedMaps对象被删除是否正常
        """
        favorite = FavoriteMaps.objects.all()[0]
        favorite.delete()
        favorite = FavoriteMaps.objects.all()
        self.assertEqual(len(favorite), 0)

    def test_delete_designed_maps_can_remove_favorite_maps(self):
        """
        测试删除DesignedMaps对象是否会导致相关的FavoriteMaps被删除
        """
        map_one = DesignedMaps.objects.all()[0]
        map_one.delete()
        map_one = DesignedMaps.objects.all()
        self.assertEqual(len(map_one), 0)
        favorite = FavoriteMaps.objects.all()
        self.assertEqual(len(favorite), 0)
