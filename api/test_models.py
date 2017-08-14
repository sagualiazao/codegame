# coding=utf-8
from django.test import TestCase
from api.models import User, GameLevels, DesignedMaps, FavoriteMaps


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(email='tom@123.com', password='123456', nickname='Tom')
        User.objects.create_user(email='jerry@123.com', password='就是汉字密码', nickname='杰瑞')

    def test_user_can_be_created(self):
        tom = User.objects.filter(email='tom@123.com')
        jerry = User.objects.filter(email='jerry@123.com')
        self.assertEqual(len(tom), 1)
        self.assertEqual(len(jerry), 1)
        self.assertTrue(tom[0].check_password('123456'))
        self.assertTrue(jerry[0].check_password('就是汉字密码'))
        self.assertEqual(tom[0].nickname, 'Tom')
        self.assertEqual(jerry[0].nickname, '杰瑞')

    def test_user_get_name(self):
        tom = User.objects.filter(email='tom@123.com')
        self.assertEqual(tom[0].get_full_name(), 'tom@123.com')
        self.assertEqual(tom[0].get_short_name(), 'tom@123.com')

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=False, password='123456', nickname='Tom')

    def test_user_default_values(self):
        tom = User.objects.get(email='tom@123.com')
        jerry = User.objects.get(email='jerry@123.com')
        self.assertFalse(tom.has_paied)
        self.assertFalse(jerry.has_paied)
        self.assertEqual(tom.game_progress, 0)
        self.assertEqual(jerry.game_progress, 0)

    def test_user_reset_password(self):
        tom = User.objects.get(email='tom@123.com')
        jerry = User.objects.get(email='jerry@123.com')
        tom.set_password('654321')
        jerry.set_password('新的汉字密码')
        self.assertTrue(tom.check_password('654321'))
        self.assertTrue(jerry.check_password('新的汉字密码'))


class GameLevelsTestCase(TestCase):
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
    def setUp(self):
        author = User.objects.create_user(email='author@123.com', nickname='author', password='123456')
        DesignedMaps.objects.create(
            map='111111',
            name='new map',
            remarks='none',
            author=author
        )

    def test_designed_maps_can_be_created(self):
        author = User.objects.get(email='author@123.com')
        map_one = DesignedMaps.objects.get(map_id=1)
        self.assertEqual(map_one.map, '111111')
        self.assertEqual(map_one.name, 'new map')
        self.assertEqual(map_one.remarks, 'none')
        self.assertEqual(map_one.author, author)
        self.assertFalse(map_one.is_published)

    def test_designed_maps_can_be_published(self):
        map_one = DesignedMaps.objects.all()[0]
        map_one.publish()
        map_one = DesignedMaps.objects.all()[0]
        self.assertTrue(map_one.is_published)

    def test_designed_maps_can_cancel_publish(self):
        map_one = DesignedMaps.objects.all()[0]
        map_one.is_published = True
        map_one.save()
        map_one.cancel_publish()
        self.assertFalse(map_one.is_published)

    def test_designed_maps_can_be_deleted(self):
        map_one = DesignedMaps.objects.all()[0]
        map_one.delete()
        map_one = DesignedMaps.objects.all()
        self.assertEqual(len(map_one), 0)


class FavoriteMapsTestCase(TestCase):
    def setUp(self):
        author = User.objects.create_user(email='author@123.com', nickname='author', password='123456')
        map_one = DesignedMaps.objects.create(
            map='111111',
            name='new map',
            remarks='none',
            author=author
        )
        FavoriteMaps.objects.create(user=author, map=map_one)

    def test_favorite_maps_can_be_created(self):
        favorite = FavoriteMaps.objects.all()[0]
        author = User.objects.get(email='author@123.com')
        map_one = DesignedMaps.objects.all()[0]
        self.assertEqual(favorite.user, author)
        self.assertEqual(favorite.map, map_one)

    def test_favorite_maps_can_be_deleted(self):
        favorite = FavoriteMaps.objects.all()[0]
        favorite.delete()
        favorite = FavoriteMaps.objects.all()
        self.assertEqual(len(favorite), 0)