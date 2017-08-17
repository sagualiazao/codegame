"""
    api的工具包
"""
import random, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import base64
from Crypto.Hash import MD5
from Crypto.Cipher import AES
import re


class Captcha:
    """
    生成验证码  
    原代码位于 http://www.cnblogs.com/skiler/p/6652848.html

    Functions:  
        string_captcha() - 生成一个随机验证码字符串
        generate_captcha() - 生成一个随机字符的图片验证码
        base64_captcha() - 生成用于发送到web前端格式的验证码
    """
    # 删除了易混淆的'O'(大写字母)
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ0123456789'

    @staticmethod
    def string_captcha(length=6):
        """
        生成一个随机验证码字符串

        Parameters:  
            length - 验证码的长度  
        
        Returns:  
            返回一个长度为length的验证码字符串
        """
        captcha_list =  random.sample(Captcha.chars, length)
        return ''.join(captcha_list)

    @staticmethod
    def generate_captcha(width=80, height=35,
        background='#FFFFFF', foreground='#FF0000',
        font_size=16, length=4, deform=False,
        draw_lines=True, n_line=(1, 2),
        draw_points=True, point_chance=2):
        """
        生成验证码图片和字符串
        
        Parameters:  
            width - 图片宽度  
            height - 图片高度  
            background - 背景色  
            foreground - 前景色  
            font_size - 字体大小  
            length - 验证码长度  
            deform - 图片扭曲  
            draw_lines - 绘制干扰线  
            n_line - 干扰线条数范围  
            draw_points - 绘制干扰点  
            point_chance - 干扰点比率
        
        Returns:  
            img - 图片验证码  
            code - 验证码字符串
        """

        # 初始化
        BASE_DIR = os.path.dirname(__file__)
        file_path = os.path.join(BASE_DIR, 'static/font/MONACO.TTF')
        font = ImageFont.truetype(file_path, font_size)

        # 创建图形
        img = Image.new('RGB', (width, height), background)
        draw = ImageDraw.Draw(img)

        # 绘制干扰线
        def create_lines():
            line_num = random.randint(*n_line)
            for i in range(line_num):
                begin = (random.randint(0, width), random.randint(0, height))
                end = (random.randint(0, width), random.randint(0, height))
                draw.line([begin, end], fill=foreground)

        # 绘制干扰点
        def create_points():
            chance = min(100, max(0, int(point_chance)))

            for w in range(width):
                for h in range(height):
                    tmp = random.randint(0, 100)
                    if tmp > 100 - chance:
                        draw.point((w, h), fill=foreground)

        # 生成给定长度的字符串，返回列表格式
        def get_chars():
            return random.sample(Captcha.chars, length)

        # 绘制验证码字符
        def create_strs():
            c_chars = get_chars()
            strs = ' %s ' % ' '.join(c_chars)
            font_width, font_height = font.getsize(strs)
            draw.text(((width - font_width) / 3, (height - font_height) / 3),
                    strs, font=font, fill=foreground)
            return ''.join(c_chars)

        if draw_lines:
            create_lines()
        if draw_points:
            create_points()
        strs = create_strs()

        if deform:
            params = [1 - float(random.randint(1, 2)) / 100,  0, 0, 0,
                    1 - float(random.randint(1, 10)) / 100, float(random.randint(1, 2)) / 500, 0.001,float(random.randint(1, 2)) / 500]
            img = img.transform((width, height), Image.PERSPECTIVE, params)

        # 返回图片和对应的字符串
        return img, strs

    @staticmethod
    def base64_captcha():
        """
        生成用于发送到web前端格式的验证码
        
        Parameters:  
            无
        
        Returns:  
            img - 图片验证码的base64编码  
            code - 验证码字符串的小写字母格式
        """
        f = BytesIO()
        img, code = Captcha.generate_captcha()
        img.save(f, 'PNG')
        img = base64.b64encode(f.getvalue()).decode()
        code = str.lower(code)
        return img, code

class CBC:
    """
    给出一种CBC加密和解密方法

    Functions:  
        crypt() - 将给定字符串加密后转换为base64编码  
        decrypt() - 将给定base64编码解密为字符串  
    """
    @staticmethod
    def crypt(key_str, data):
        """
        将给定字符串加密

        Parameters:  
            key_str - 用于加密的密钥  
            data - 要被加密的字符串  
        
        Returns:  
            crypted_str - 加密后的数据的base64编码
        """
        params_is_str = isinstance(key_str, str) and isinstance(data, str)
        if params_is_str:
            # 生成秘钥的字符串,可以用验证码
            key_md5 = MD5.new()
            key_md5.update(bytes(key_str, 'utf-8'))
            # 可以用于AES的key
            key_str = key_md5.hexdigest()
            # 可以用于AES的iv
            iv_str = key_str[2:18]
            # python需要使用'\0'来填充,否则加密得到的结果会和js加密结果不同
            padding = '\0'
            pad_it = lambda s: s + (16 - len(bytes(s, 'utf-8')) % 16) * padding
            generator = AES.new(key_str, AES.MODE_CBC, iv_str)
            crypted_bytes = generator.encrypt(pad_it(data))
            crypted_str = base64.b64encode(crypted_bytes).decode()
            return crypted_str
        else:
            raise TypeError('加密仅接受字符串参数')

    @staticmethod
    def decrypt(key_str, data):
        """
        将给定加密后的字符串解密

        Parameters:  
            key_str - 用于解密的密钥  
            data - 加密后的base64字符串  

        Returns:  
            recovery_str - 解密后的字符串
        """
        params_is_str = isinstance(key_str, str) and isinstance(data, str)
        if params_is_str:
            key_md5 = MD5.new()
            key_md5.update(bytes(key_str, 'utf-8'))
            key_str = key_md5.hexdigest()
            iv_str = key_str[2:18]
            padding = '\0'
            generator = AES.new(key_str, AES.MODE_CBC, iv_str)
            data = base64.b64decode(data)
            recovery = generator.decrypt(data)
            recovery_str = recovery.decode().rstrip(padding)
            return recovery_str
        else:
            raise TypeError('加密仅接受字符串参数')


def check_email_format(email):
    """
    检查邮箱格式
    """
    pattern = re.compile(r'^[a-z0-9]+([._\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$')
    if pattern.match(email) != None:
        return True
    else:
        return False


class MapImage:
    """
    生成地图缩略图
    """
    # 需要保证当前工作目录在Group1
    RESOURCE_DIR = './api/static/map/'
    MAP_DIR = './api/static/img/saved_maps/'
    RESOURCE_WIDTH = 64
    RESOURCE_HEIGHT = 64
    GRIDS_PER_ROW = 10
    GRIDS_PER_COLUMN = 10
    # BACKGROUND = (0, 255, 0)
    SOURCE_LIST = [
        RESOURCE_DIR + 'background.png',  # 0: background
        RESOURCE_DIR + '1.png',  # 1: tree
        RESOURCE_DIR + '2.png',  # 2: river
        RESOURCE_DIR + '3.png',  # 3: player
        RESOURCE_DIR + '4.png',  # 4: flag
        RESOURCE_DIR + '5.png',  # 5: transform
    ]
    MAP_SIZE = GRIDS_PER_COLUMN * GRIDS_PER_ROW

    @staticmethod
    def generate_map_image(map_id, map_str, scale=0.25):
        """
        生成地图缩略图并保存在MAP_DIR目录下

        Parameters:  
            map_id - 地图的id号,用于生成文件名  
            map_str - 地图的内容字符串
            scale - 缩放比率
        Returns:  
            True - 生成缩略图成功
            False - 资源丢失,生成缩略图失败
        """
        def paste_resource_onto_map(char, index, image):

            def char_to_resource(char):
                switcher = {
                    '1': 1,  # 1: tree
                    '2': 2,  # 2: river
                    '3': 3,  # 3: player
                    '4': 4,  # 4: flag
                    '5': 5,  # 5: transform
                }
                return switcher.get(char, None)

            if char == '0':
                return
            else:
                row = index // MapImage.GRIDS_PER_ROW
                column = index % MapImage.GRIDS_PER_COLUMN
                box = (
                    row * MapImage.RESOURCE_WIDTH,
                    column * MapImage.RESOURCE_HEIGHT,
                )
                image.alpha_composite(resources[char_to_resource(char)], dest=box)

        map_str = map_str
        map_id = map_id
        scale = scale
        map_width = MapImage.RESOURCE_WIDTH * MapImage.GRIDS_PER_ROW
        map_height = MapImage.RESOURCE_HEIGHT * MapImage.GRIDS_PER_COLUMN
        the_map = Image.new('RGBA', (map_width, map_height))
        resources = list()
        try:
            for resource_img in MapImage.SOURCE_LIST:
                resources.append(Image.open(resource_img))
        except FileNotFoundError:
            return False
        else:
            the_map.paste(resources[0], (0, 0, map_width, map_height))
            # 把记录传送坐标的一组数字转换为单一数字
            map_str = re.sub(r'!\d\d!', '5', map_str)

            for i in range(MapImage.MAP_SIZE):
                paste_resource_onto_map(map_str[i], i, the_map)

            the_map = the_map.resize((int(map_width * scale), int(map_height * scale)))
            file_name = str(map_id) + '.png'

            if not os.path.exists(MapImage.MAP_DIR):
                os.makedirs(MapImage.MAP_DIR)
            the_map.save(MapImage.MAP_DIR + file_name, 'PNG')
            return True