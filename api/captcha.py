'''
生成图片验证码
原代码位于 http://www.cnblogs.com/skiler/p/6652848.html
'''
import random, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

class Captcha:
    '''
        generate_captcha() 生成验证码图片和对应的字符串\n
        string_captcha() 生成验证码字符串
    '''
    # 删除了易混淆的'O'(大写字母)
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ0123456789'

    def string_captcha():
        '''
            @return 一个长度为6的验证码字符串
        '''
        return random.sample(Captcha.chars, 6)

    def generate_captcha(width=120, height=50,
        background='#FFFFFF', foreground='#0000FF',
        font_size=18, length=4,
        draw_lines=True, n_line=(1, 2),
        draw_points=True, point_chance=2):
        '''
            生成一个四位随机字符的图片验证码\n
            @return :img:验证码的图片, :str: 验证码的字符串
        '''

        # 初始化
        BASE_DIR = os.path.dirname(__file__)
        file_path = os.path.join(BASE_DIR, 'static/font/MONACO.TTF')
        font = ImageFont.truetype(file_path, font_size)

        # 创建图形
        img = Image.new('RGB', (width, height), background)
        draw = ImageDraw.Draw(img)  # 创建画笔

        # 绘制干扰线
        def create_lines():
            line_num = random.randint(*n_line)  # 干扰线条数

            for i in range(line_num):
                # 起始点
                begin = (random.randint(0, width), random.randint(0, height))
                # 结束点
                end = (random.randint(0, width), random.randint(0, height))
                draw.line([begin, end], fill=foreground)

        # 绘制干扰点
        def create_points():
            chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]

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
            strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开

            font_width, font_height = font.getsize(strs)

            draw.text(((width - font_width) / 3, (height - font_height) / 3),
                    strs, font=font, fill=foreground)

            return ''.join(c_chars)

        if draw_lines:
            create_lines()
        if draw_points:
            create_points()
        strs = create_strs()

        # 图形扭曲参数
        params = [1 - float(random.randint(1, 2)) / 100,  0, 0, 0,
                1 - float(random.randint(1, 10)) / 100, float(random.randint(1, 2)) / 500, 0.001,float(random.randint(1, 2)) / 500]
        # 创建扭曲
        img = img.transform((width, height), Image.PERSPECTIVE, params)

        # 返回图片和对应的字符串
        return img, strs