"""
    API工具包,定义了一些在服务器API中使用的函数
"""
import random, os, base64, re, pingpp, string
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
from Crypto.Hash import MD5
from Crypto.Cipher import AES
from django.http import JsonResponse
import api.models


class SimpleResponse:
    """
    用于简化创建json回应消息的代码
    """
    failure_json_response = JsonResponse({'status': '0'})
    """ 一个表明失败状态的json响应 """
    success_json_response = JsonResponse({'status': '1'})
    """ 一个表明成功状态的json响应 """

    @staticmethod
    def user_json_response(user):
        """
        返回指定用户对象信息的JsonResponse

        Parameters:
            :user: 用户对象\n
        
        Returns:
            JsonResponse:\n
            :'status': 登录失败'0', 登录成功'1'\n
            :'email': 用户的电子邮件\n
            :'nickname': 用户的昵称\n
            :'id': - 用户的id\n
            :'gameProgress': 用户的游戏进度\n
            :'hasPaied': 用户是否已经付费\n
        """
        return JsonResponse({
            'status': '1',
            'email': user.email,
            'nickname': user.nickname,
            'id': user.id,
            'gameProgress': user.game_progress,
            'hasPaied': user.has_paied,
            'createdAt': user.created_at
        })

    @staticmethod
    def designed_map_json_response(selected_map):
        """
        返回指定地图对象信息的JsonResponse

        Parameters:
            :user: 用户对象\n
        
        Returns:
            JsonResponse:\n
            :'status': 读取失败'0', 读取成功'1'\n
            :'map': 地图字符串\n
            :'name': 地图名\n
            :'remarks': 地图说明\n
            :'author': 地图作者\n
            :'is_published': 地图发布状态\n
        """
        return JsonResponse({
            'status': '1',
            'map': selected_map.map,
            'name': selected_map.name,
            'remarks': selected_map.remarks,
            'author': str(selected_map.author)
        })


class Captcha:
    """
    生成验证码

    原代码位于 http://www.cnblogs.com/skiler/p/6652848.html
    """

    CHAR_SETS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ0123456789'
    """ 用于生成验证码的字符集 """

    @staticmethod
    def string_captcha(length=6):
        """
        生成一个随机验证码字符串

        Parameters:  
            :length: 验证码的长度\n
        
        Returns:  
            :captcha: 长度为length的验证码字符串\n
        """
        captcha_list =  random.sample(Captcha.CHAR_SETS, length)
        captcha = ''.join(captcha_list)
        return captcha

    @staticmethod
    def generate_captcha(width=80, height=35,
        background='#FFFFFF', foreground='#FF0000',
        font_size=16, length=4, deform=False,
        draw_lines=True, n_line=(1, 2),
        draw_points=True, point_chance=2):
        """
        生成验证码图片和字符串
        
        Parameters:  
            :width: 图片宽度\n
            :height: 图片高度\n
            :background: 背景色\n
            :foreground: 前景色\n
            :font_size: 字体大小\n
            :length: 验证码长度\n
            :deform: 图片扭曲\n
            :draw_lines: 绘制干扰线\n
            :n_line: 干扰线条数范围\n            
            :draw_points: 绘制干扰点\n
            :point_chance: 干扰点比率\n

        Returns:  
            :img: 图片验证码\n
            :strs: 验证码字符串\n
        """

        BASE_DIR = os.path.dirname(__file__)
        file_path = os.path.join(BASE_DIR, 'static/font/MONACO.TTF')
        font = ImageFont.truetype(file_path, font_size)
        img = Image.new('RGB', (width, height), background)
        draw = ImageDraw.Draw(img)

        def create_lines():
            """
            绘制干扰线
            """
            line_num = random.randint(*n_line)
            for i in range(line_num):
                begin = (random.randint(0, width), random.randint(0, height))
                end = (random.randint(0, width), random.randint(0, height))
                draw.line([begin, end], fill=foreground)

        def create_points():
            """
            绘制干扰点
            """
            chance = min(100, max(0, int(point_chance)))

            for w in range(width):
                for h in range(height):
                    tmp = random.randint(0, 100)
                    if tmp > 100 - chance:
                        draw.point((w, h), fill=foreground)

        
        def get_chars():
            """
            生成给定长度的字符串列表
            """
            return random.sample(Captcha.CHAR_SETS, length)

        def create_strs():
            """
            绘制验证码字符
            """
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

        return img, strs

    @staticmethod
    def base64_captcha():
        """
        生成base64编码的验证码图片,返回web前端
        
        Parameters:  
            无
        
        Returns:  
            :img: 图片验证码的base64编码\n
            :code: 验证码字符串的小写字母格式\n
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
    """
    @staticmethod
    def crypt(key_str, data):
        """
        将给定字符串加密

        Parameters:  
            :key_str: 用于加密的密钥\n
            :data: 要被加密的字符串\n
        
        Returns:  
            :crypted_str: 加密后的数据的base64编码\n
        """
        params_is_str = isinstance(key_str, str) and isinstance(data, str)
        if params_is_str:
            key_md5 = MD5.new()
            key_md5.update(bytes(key_str, 'utf-8'))
            key_str = key_md5.hexdigest()
            iv_str = key_str[2:18]
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
            :key_str: 用于解密的密钥\n
            :data: 加密后的base64字符串\n

        Returns:  
            :recovery_str: 解密后的字符串\n
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

    Parameters:
        :email: 给定的email\n

    Returns:
        :True/False: email符合规范返回True,否则返回False\n
    """
    pattern = re.compile(r'^[a-z0-9]+([._\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$')
    if pattern.match(email.lower()) != None:
        return True
    else:
        return False


class MapImage:
    """
    生成地图缩略图
    """
    RESOURCE_DIR = './api/static/map/'
    """ 地图资源目录 """
    MAP_DIR = './api/static/img/saved_maps/'
    """ 地图存储目录 """
    RESOURCE_WIDTH = 64
    """ 资源宽度 """
    RESOURCE_HEIGHT = 64
    """ 资源高度 """
    GRIDS_PER_ROW = 10
    """ 每行方格数 """
    GRIDS_PER_COLUMN = 10
    """ 每列方格数 """
    SOURCE_LIST = [
        RESOURCE_DIR + 'background.png',  # 0: background
        RESOURCE_DIR + '1.png',  # 1: tree
        RESOURCE_DIR + '2.png',  # 2: river
        RESOURCE_DIR + '3.png',  # 3: player
        RESOURCE_DIR + '4.png',  # 4: flag
        RESOURCE_DIR + '5.png',  # 5: transform
    ]
    """ 地图资源列表 """
    MAP_SIZE = GRIDS_PER_COLUMN * GRIDS_PER_ROW
    """ 地图大小 """

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


class Pingpp:
    """
    Ping++ 实现的支付接口\n
    因为没有营业执照只能使用test模式\n
    """
    @staticmethod
    def pay():
        """
        模拟一个支付请求

        Paramters:
            无

        Returns:
            :str: 模拟支付请求返回的url
        """
        api_key = 'sk_test_uDWrjHf5aznDjL8mrDWLK4m9'
        app_id = 'app_4Si9mDSOGmv90Wjf'
        pingpp.api_key = api_key
        pingpp.private_key = '''-----BEGIN RSA PRIVATE KEY-----
        MIIEowIBAAKCAQEAx2MktxcKBEqdYRi2IgYcupPQIN5cxgiBL5udCCBJBNBbXPaq
        uOE1qspfhB1KUzHXATnCONiSzubLcBTnwi2tz0ErRCeJZSERRCpbKx4eu6b1neUT
        Wkga7xpZxWONEvkmZo5Nlhf4fXRPUYnO/bdGCNGpQ/HSJfWLtzmhCqO1aJwVhcDm
        DMYz4bTkZavhFBdVyXf/8n7UKylk03eymlKJ1swQpeFcxaKfzsk1mJU7mc93mCWj
        aR+VWkNbw4AQHDyHgbzH+zYARzCluiy5hXdixGEP+iO4ZBk48rEs1hKTvGz1k+jh
        LCdkdpBRjq0pK/htjA3Ce8pF2AJs+fgN6ZUumQIDAQABAoIBAFa4MEfRpXGoYjrQ
        3KZ/sg8UKvmgvQkEuetS60GViSym0pXkUuyGRyk5S8HSW3lDvBe0X10KFRAYIXNm
        JEa4R1hVJ9REveVWNIRJR83BE+zZ+QnrkDc8FTrZYyIO4lTWOHVyfxxA4Lrv02/L
        WFPRWoyLY+tBSf1ohpPyZLCT81rDglT1Z4svX020y8tXvnQqQiOjl4q7Zu4b26HU
        TQ463ntMEhM5u7y9MFcxGRaOpF/gARlMGqDu6T8h/oYMiOSLoXOuTR7B80yaX/Mj
        RZfUBoZMb5thX9qBLQ7dYnTkwaxwerYPrYvQrW9vtsswZ5NeIbEmCZyorUe8DOmQ
        hT1+HmECgYEA/iQERHhZKHXnP0gvhl/uEOGOvLjD5H1D6zClzOHMmOcIF5OuEQb0
        VcSMV+8emN7SCp/b/LVgKa27Mla9eXm+EXABRFcI7qGYsYXfbCD7EYX3TaJSp/30
        jyLBy+MsHCTEiLeylSh7kHqgTR8tKND8UIzXo9aM7JqwFqleeXGyh7MCgYEAyNiU
        EUzyBAv9sui3ZgVYRiVvTilk2HVTY6u61/mMOLsTrX3eYQaqb4GRJJShJO9mmsxX
        RHBEZQJvUqqF9PapOsyv8HKuF5+UP6svHnJo7sn9gCvV/h1HTHqzFcYSvUaXnrym
        D/0Tthf8CDeuGp5UFWMoFZF14HTr1oQROGAASoMCgYA0bZmzxmAeSLR8CZhEUGX8
        dYvMwxEmgfERA+gwbCSZJpA0zPKL8LNXPkT1nw7g2pbaOkBX0dMUxhJoQBy2grcD
        QegBATOGhy/I76U32VXyN4DdMy96GJnrLXBtb2AaLjudOMhOnRtgouuO/W+DjBmB
        RIz377sC1KafBjHHO/1ooQKBgDQqfJrZv2ppquVTKH9pF/pwMq68daL7JkOXERqT
        iGYbwQqozJ+q2Y3Iu2gi6o/rVl0SggAWoM0TitKP0+dCQcYx7+imAK3GFv1KexyP
        Xs3WzO8Dc7ti42fr3qPjJG7g7PSfzwoME5iSNjX0MFZdlT1Q2dJwS4uXEsJO3yIj
        XS/9AoGBALRApgtUA7Odw4tjCLGvxXuLFnyRkg6hFqoXAP2j8H9bJDOlSSVwQTFd
        ahbcIDtQJS57vXUGK2uspbFKLm1WCFzPVyuxDIW6oue/kO+YxxU3NA58zk8oaORq
        eA3YvHc7ZmRjVnVkxnXjKofrL6jF5A+lXSXnXchrv2ZYI+1pOsIV
        -----END RSA PRIVATE KEY-----'''
        orderno = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        try:
            ch = pingpp.Charge.create(
                subject='Your Subject',
                body='Your Body',
                amount=100,
                order_no=orderno,
                currency='cny',
                channel='alipay_qr',
                client_ip='127.0.0.1',
                app=dict(id=app_id)
            )
            return ch.credential.alipay_qr
        except Exception as e:
            print(e.message)
