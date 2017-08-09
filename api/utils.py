'''
    api的工具包
'''
import random, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import base64
from Crypto.Hash import MD5
from Crypto.Cipher import AES


class Captcha:
    '''
    生成验证码  
    原代码位于 http://www.cnblogs.com/skiler/p/6652848.html

    Functions:  
        string_captcha() - 生成一个随机验证码字符串
        generate_captcha() - 生成一个随机字符的图片验证码
        base64_captcha() - 生成用于发送到web前端格式的验证码
    '''
    # 删除了易混淆的'O'(大写字母)
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ0123456789'

    def string_captcha(length=6):
        '''
        生成一个随机验证码字符串

        Parameters:  
            length - 验证码的长度  
        
        Returns:  
            返回一个长度为length的验证码字符串
        '''
        return random.sample(Captcha.chars, length)

    def generate_captcha(width=80, height=35,
        background='#FFFFFF', foreground='#FF0000',
        font_size=16, length=4, deform=False,
        draw_lines=True, n_line=(1, 2),
        draw_points=True, point_chance=2):
        '''
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
        '''

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

    def base64_captcha():
        '''
        生成用于发送到web前端格式的验证码
        
        Parameters:  
            无
        
        Returns:  
            img - 图片验证码的base64编码  
            code - 验证码字符串的小写字母格式
        '''
        f = BytesIO()
        img, code = Captcha.generate_captcha()
        img.save(f, 'PNG')
        img = base64.b64encode(f.getvalue()).decode()
        code = str.lower(code)
        return img, code

class CBC:
    '''
    给出一种CBC加密和解密方法

    Functions:  
        crypt() - 将给定字符串加密后转换为base64编码  
        decrypt() - 将给定base64编码解密为字符串  
    '''
    def crypt(key_str, data):
        '''
        将给定字符串加密

        Parameters:  
            key_str - 用于加密的密钥  
            data - 要被加密的字符串  
        
        Returns:  
            crypted_str - 加密后的数据的base64编码
        '''
        # 生成秘钥的字符串,可以用验证码
        key_md5 = MD5.new()
        key_md5.update(bytes(key_str, 'utf-8'))
        # 可以用于AES的key
        key_str = key_md5.hexdigest()
        # 可以用于AES的iv
        iv_str = key_str[2:18]
        # python需要使用'\0'来填充,否则加密得到的结果会和js加密结果不同
        padding = '\0'
        pad_it = lambda s: s + (16 - len(s) % 16) * padding
        generator = AES.new(key_str, AES.MODE_CBC, iv_str)
        crypted_bytes = generator.encrypt(pad_it(data))
        crypted_str = base64.b64encode(crypted_bytes).decode()
        return crypted_str

    def decrypt(key_str, data):
        '''
        将给定加密后的字符串解密

        Parameters:  
            key_str - 用于解密的密钥  
            data - 加密后的base64字符串  

        Returns:  
            recovery_str - 解密后的字符串
        '''
        key_md5 = MD5.new()
        key_md5.update(bytes(key_str, 'utf-8'))
        key_str = key_md5.hexdigest()
        iv_str = key_str[2:18]
        padding = '\0'
        pad_it = lambda s: s + (16 - len(s) % 16) * padding
        generator = AES.new(key_str, AES.MODE_CBC, iv_str)
        data = base64.b64decode(data)
        recovery = generator.decrypt(data)
        recovery_str = recovery.decode().rstrip(padding)
        return recovery_str

