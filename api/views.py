from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
import simplejson
from api.utils import *
from django.core.mail import send_mail
from api.models import User, DesignedMaps, GameLevels, FavoriteMaps


def get_captcha(request):
    """
    向web前端发送图片验证码

    Parameters:
        :request: 指向'/api/captcha'的GET请求\n

    Returns:
        JsonResponse:\n
        :'img': 图片验证码的base64编码\n
        :'capthca': 验证码的小写字符串\n

        HttpResponseNotFound(): 如果request不是一个GET请求\n
    """
    def get_captcha_function(request):
        img, code = Captcha.base64_captcha()
        return JsonResponse({
            'img': img,
            'captcha': code,
        })

    return SimpleResponse.get_only(request, get_captcha_function)


@csrf_exempt
def register(request):
    """
    执行注册用户操作

    Parameters:
        :request: 指向'/api/register'的POST请求\n

    Returns:
        JsonResponse:\n
        :'status': 注册失败'0', 注册成功'1'\n
        :'capthca': 验证码的小写字符串\n

        HttpResponseNotFound(): 如果request不是一个POST请求\n
    """
    def register_fuction(request):
        req = simplejson.load(request)
        email = req['email']
        if check_email_format(email) == False:
            return SimpleResponse.failure_json_response
        if len(User.objects.filter(email=email)) > 0:
            return SimpleResponse.failure_json_response
        password_ace = req['password']
        nickname = req['nickname']
        captcha = req['captcha']
        password = CBC.decrypt(captcha, password_ace)
        User.objects.create_user(email=email, nickname=nickname, password=password)
        return SimpleResponse.success_json_response

    return SimpleResponse.post_only(request, register_fuction)


@csrf_exempt
def reset_password_email(request):
    """
    发送重置密码的邮件验证码

    Parameters:
        :request: 指向'/api/reset-password-email'的POST请求\n

    Returns:
        JsonResponse:\n
        :'status': 发送失败'0', 发送成功'1'\n
        :'capthca': 验证码的小写字符串\n

        HttpResponseNotFound(): 如果request不是一个POST请求\n
    """
    def reset_password_email_function(request):
        req = simplejson.load(request)
        email = req['email']
        users = User.objects.filter(email=email)
        if len(users) == 0:
            return SimpleResponse.failure_json_response
        captcha = Captcha.string_captcha()
        msg = '您重置账户: [' + email + '] 密码的验证码是: ' + captcha
        mail_status = send_mail(
            r'[验证码]仨瓜俩枣小组的编程游戏-密码重置',
            msg,
            'sagualiazao@aliyun.com',
            [email],
            fail_silently=False
        )
        request.session['captcha'] = captcha
        return SimpleResponse.success_json_response

    return SimpleResponse.post_only(request, reset_password_email_function)


def check_email_captcha(request):
    """
    建议输入的邮件验证码是否正确

    Parameters:
        :request: 指向'/api/check-email'的GET请求\n

    Returns:
        JsonResponse:\n
        :'status': 未被注册'0', 已被注册'1'\n

        HttpResponseNotFound(): 如果request不是一个GET请求\n
    """
    def check_email_captcha_function(request):
        captcha = request.GET['captcha']
        if captcha != request.session['captcha']:
            return SimpleResponse.failure_json_response
        else:
            return SimpleResponse.success_json_response

    return SimpleResponse.get_only(request, check_email_captcha_function)


@csrf_exempt
def reset_password(request):
    """
    重置密码

    Parameters:
        :request: 指向'/api/reset-password'的POST请求\n

    Returns:
        JsonResponse:\n
        :'status': 修改失败'0', 修改成功'1'\n

        HttpResponseNotFound(): 如果request不是一个POST请求\n
    """
    def reset_password_function(request):
        req = simplejson.load(request)
        email = req['email']
        users = User.objects.filter(email=email)
        if len(users) == 0:
            return SimpleResponse.failure_json_response
        password_ace = req['password']
        captcha = req['captcha']
        password = CBC.decrypt(captcha, password_ace)
        user = users[0]
        user.set_password(password)
        user.save()
        return SimpleResponse.success_json_response

    return SimpleResponse.post_only(request, reset_password_function)


@csrf_exempt
def login(request):
    """
    登录

    Parameters:
        :request: 指向'/api/login'的POST请求或GET请求\n
    Returns:
        JsonResponse:\n
        :'status': 登录失败'0', 登录成功'1'\n
        :'email': 用户的电子邮件\n
        :'nickname': 用户的昵称\n
        :'id': - 用户的id\n
        :'gameProgress': 用户的游戏进度\n
        :'hasPaied': 用户是否已经付费\n

        HttpResponseNotFound(): 如果request不是一个POST\GET请求\n
    """
    def login_get_fuction(request):
        email = request.session.get('email', False)
        if email == False:
            return SimpleResponse.failure_json_response
        else:
            users = User.objects.filter(email=email)
            user = users[0]
            return SimpleResponse.user_json_response(user)

    def login_post_function(request):
        req = simplejson.load(request)
        email = req['email']
        users = User.objects.filter(email=email)
        if len(users) == 0:
            return SimpleResponse.failure_json_response
        password_ace = req['password']
        captcha = req['captcha']
        password = CBC.decrypt(captcha, password_ace)
        user = users[0]
        login_status = user.check_password(password)
        if login_status:
            request.session['email'] = email
            return SimpleResponse.user_json_response(user)
        else:
            return SimpleResponse.failure_json_response

    return SimpleResponse.get_or_post(request, login_get_fuction, login_post_function)


def check_email(request):
    """
    检验邮箱是否已被注册

    Parameters:
        :request: 指向'/api/check-email'的GET请求\n

    Returns:
        JsonResponse:\n
        :'status': - 未被注册'0', 已被注册'1'\n

        HttpResponseNotFound(): 如果request不是一个GET请求\n
    """
    def check_email_function(request):
        email = request.GET['email']
        users = User.objects.filter(email=email)
        if len(users) == 0:
            return SimpleResponse.failure_json_response
        else:
            return SimpleResponse.success_json_response

    return SimpleResponse.get_only(request, check_email_function)


def logout(request):
    """
    注销

    Parameters:
        :request: 指向'/api/logout'的GET请求\n

    Returns:
        JsonResponse:\n
        :'status': 注销失败'0', 注销成功'1'\n

        HttpResponseNotFound(): 如果request不是一个GET请求\n
    """
    if request.method == 'GET':
        email = request.session.get('email', False)
        if email == False:
            return SimpleResponse.failure_json_response
        else:
            del request.session['email']
            return SimpleResponse.success_json_response
    else:
        return HttpResponseNotFound()


@csrf_exempt
def save_map(request):
    """
    保存用户编辑的地图

    Parameters:
        :request: 指向'/api/save-map'的POST请求\n
        :mapString: 要存储的地图信息\n
        :name: 地图的名称\n
        :remarks: 地图的说明\n

    Returns:
        JsonResponse:\n
        :'status': 保存失败'0', 保存成功'1'\n

        HttpResponseNotFound(): 如果request不是一个POST请求\n
    """
    def save_map_function(request):
        req = simplejson.load(request)
        email = request.session['email']
        author = User.objects.get(email=email)
        map_str = req['mapString']
        name = req['name']
        remarks = req['remarks']
        new_map = DesignedMaps(
            map=map_str,
            name=name,
            remarks=remarks,
            author=author,
            is_published=False
        )
        new_map.save()
        status = MapImage.generate_map_image(new_map.map_id, map_str)
        return SimpleResponse.success_json_response
    
    return SimpleResponse.post_only(request, save_map_function)


def read_map(request):
    """
    读取用户编辑的地图

    Parameters:
        :request: 指向'/api/read-map'的GET请求\n
        :mapid: 要读取的map的id\n

    Returns:
        JsonResponse:\n
        :'status': 读取失败'0', 读取成功'1'\n
        :'map': 地图字符串\n
        :'name': 地图名\n
        :'remarks': 地图说明\n
        :'author': 地图作者\n
        :'is_published': 地图发布状态\n

        HttpResponseNotFound(): 如果request不是一个GET请求\n
    """
    def read_map_function(request):
        map_id = int(request.GET['mapid'])
        selected_map = DesignedMaps.objects.filter(map_id=map_id)
        if len(selected_map) == 0:
            return SimpleResponse.failure_json_response
        else:
            selected_map = selected_map[0]
            return SimpleResponse.designed_map_json_response(selected_map)

    return SimpleResponse.get_only(request, read_map_function)


def read_level(request):
    """
    读取系统关卡

    Parameters:
        :request: 指向'/api/read-level'的GET请求\n
        :mapid: 要读取的level的id\n

    Returns:
        JsonResponse:\n
        :'status': 读取失败'0', 读取成功'1'\n
        :'map': 地图字符串\n
        :'name': 地图名\n
        :'remarks': 地图说明\n
        :'author': 地图作者\n
        :'is_published': 地图发布状态\n

        HttpResponseNotFound(): 如果request不是一个GET请求\n
    """
    def read_level_function(request):
        map_id = int(request.GET['mapid'])
        selected_map = GameLevels.objects.filter(map_id=map_id)
        if len(selected_map) == 0:
            return SimpleResponse.failure_json_response
        else:
            selected_map = selected_map[0]
            return SimpleResponse.game_level_json_response(selected_map)

    return SimpleResponse.get_only(request, read_level_function)


def pay(request):
    """
    发送支付请求

    Parameters:
        :request: 指向'/api/pay'的GET请求,需要服务器保存session信息(已登录)才能访问\n

    Returns:
        JsonResponse:\n
        :'status': 发送支付请求失败'0',发送成功'1'\n
        :'url': 成功发送支付请求打开的页面\n
    """
    def pay_function(request, email):
        users = User.objects.filter(email=email)
        user = users[0]
        alipay_pr = Pingpp.pay()
        return JsonResponse({
            'status': '1',
            'url': alipay_pr
        })

    return SimpleResponse.get_only(request, pay_function, True)


def read_map_list(request):
    """
    读取地图广场

    Parameters:
        :request: 指向'/api/read-map-list'的GET请求,需要服务器保存session信息(已登录)才能访问\n

    Returns:
        JsonResponse:\n
        :'status': 读取失败'0',读取成功'1'\n
        :'data': 读取的地图信息列表\n
    """
    def read_map_list_function(request, email):
        user = User.objects.get(email=email)
        maps = DesignedMaps.objects.filter(is_published=True)
        if len(maps) == 0:
            return JsonResponse({
                'status': '1',
                'data': ''
            })
        map_list = list()
        for i in maps:
            is_favorite_map = FavoriteMaps.objects.filter(user=user, map=i)
            map_list.append((
                i.map_id,
                i.name,
                str(i.author),
                MapImage.getImageLink(i.map_id),
                i.remarks,
                bool(len(is_favorite_map))
            ))
        json = simplejson.dumps(map_list)
        return JsonResponse({
            'status': '1',
            'number': len(map_list),
            'data': json
        })

    return SimpleResponse.get_only(request, read_map_list_function, True)


def read_my_map_list(request):
    """
    读取用户的地图

    Parameters:
        :request: 指向'/api/read-my-map-list'的GET请求,需要服务器保存session信息(已登录)才能访问\n

    Returns:
        JsonResponse:\n
        :'status': 读取失败'0',读取成功'1'\n
        :'data': 读取的地图信息列表\n
    """
    def read_my_map_list_function(request, email):
        user = User.objects.get(email=email)
        maps = DesignedMaps.objects.filter(author=user)
        if len(maps) == 0:
            return JsonResponse({
                'status': '1',
                'data': ''
            })
        map_list = list()
        for i in maps:
            map_list.append((
                i.map_id,
                i.name,
                MapImage.getImageLink(i.map_id),
                i.remarks,
                i.is_published
            ))
        json = simplejson.dumps(map_list)
        return JsonResponse({
            'status': '1',
            'number': len(map_list),
            'data': json
        })

    return SimpleResponse.get_only(request, read_my_map_list_function, True)


@csrf_exempt
def change_favorite_map(request):
    """
    修改地图收藏状态

    Parameters:
        :request: 指向'/api/change-favorite-map'的POST请求,需要服务器保存session信息(已登录)才能访问\n

    Returns:
        JsonResponse:\n
        :'status': 修改失败'0',修改成功'1'\n
    """
    def change_favorite_map_function(request, email):
        print(email)
        user = User.objects.get(email=email)
        req = simplejson.load(request)
        map_id = req['mapid']
        status = bool(int(req['status']))
        the_map = DesignedMaps.objects.get(map_id=map_id)
        has_favorite = FavoriteMaps.objects.filter(user=user, map=the_map)
        if status and len(has_favorite) == 0:
            new_favorite = FavoriteMaps(user=user, map=the_map)
            new_favorite.save()
        else:
            remove_favorite = FavoriteMaps.objects.get(user=user, map=the_map)
            remove_favorite.delete()
        json = simplejson.dumps(map_list)
        return SimpleResponse.success_json_response

    return SimpleResponse.post_only(request, change_favorite_map_function, True)


def read_published_map_list(request):
    """
    读取用户制作的地图列表

    Parameters:
        :request: 指向'/api/read-published-map-list'的GET请求,需要服务器保存session信息(已登录)才能访问\n

    Returns:
        JsonResponse:\n
        :'status': 读取失败'0',读取成功'1'\n
        :'data': 读取的地图信息列表\n
    """
    def read_published_map_list_function(request, email):
        user = User.objects.get(email=email)
        maps = DesignedMaps.objects.filter(author=user, is_published=True)
        if len(maps) == 0:
            return JsonResponse({
                'status': '1',
                'data': ''
            })
        map_list = list()
        for i in maps:
            map_list.append((
                i.map_id,
                i.name,
                MapImage.getImageLink(i.map_id),
                i.remarks
            ))
        json = simplejson.dumps(map_list)
        return JsonResponse({
            'status': '1',
            'number': len(map_list),
            'data': json
        })

    return SimpleResponse.get_only(request, read_published_map_list_function, True)


def read_favorite_map_list(request):
    """
    读取用户收藏的地图列表

    Parameters:
        :request: 指向'/api/read-favorite-map-list'的GET请求,需要服务器保存session信息(已登录)才能访问\n

    Returns:
        JsonResponse:\n
        :'status': 读取失败'0',读取成功'1'\n
        :'data': 读取的地图信息列表\n
    """
    def read_favorite_map_list_function(request, email):
        user = User.objects.get(email=email)
        favorites = FavoriteMaps.objects.filter(user=user)
        if len(favorites) == 0:
            return JsonResponse({
                'status': '1',
                'data': ''
            })
        map_list = list()
        for i in favorites:
            map_list.append((
                i.map.map_id,
                i.map.name,
                str(i.map.author),
                MapImage.getImageLink(i.map.map_id),
                i.map.remarks                        
            ))
        json = simplejson.dumps(map_list)
        return JsonResponse({
            'status': '1',
            'number': len(map_list),
            'data': json
        })

    return SimpleResponse.get_only(request, read_favorite_map_list_function, True)


@csrf_exempt
def change_publish_status(request):
    """
    修改地图发布状态

    Parameters:
        :request: 指向'/api/change-publish'的POST请求,需要服务器保存session信息(已登录)才能访问\n

    Returns:
        JsonResponse:\n
        :'status': 修改失败'0',修改成功'1'\n
    """
    def change_publish_status_function(request, email):
        user = User.objects.get(email=email)
        req = simplejson.load(request)
        map_id = req['mapid']
        status = bool(int(req['status']))
        the_map = DesignedMaps.objects.get(map_id=map_id)
        if status and the_map.author == user:
            the_map.publish()
        else:
            the_map.cancel_publish()
        return SimpleResponse.success_json_response

    return SimpleResponse.post_only(request, change_publish_status_function, True)


@csrf_exempt
def delete_map(request):
    """
    删除地图

    Parameters:
        :request: 指向'/api/delete-map'的POST请求,需要服务器保存session信息(已登录)才能访问\n

    Returns:
        JsonResponse:\n
        :'status': 修改失败'0',修改成功'1'\n
    """
    def delete_map_function(request, email):
        user = User.objects.get(email=email)
        req = simplejson.load(request)
        map_id = req['mapid']
        the_map = DesignedMaps.objects.get(map_id=map_id)
        if the_map.author == user:
            the_map.delete()
            MapImage.deleteMapImages(map_id)
        return SimpleResponse.success_json_response

    return SimpleResponse.post_only(request, delete_map_function, True)


@csrf_exempt
def change_nickname(request):
    """
    修改昵称

    Parameters:
        :request: 指向'/api/change-nickname'的POST请求,需要服务器保存session信息(已登录)才能访问\n

    Returns:
        JsonResponse:\n
        :'status': 修改失败'0',修改成功'1'\n
    """
    def change_nickname_function(request, email):
        user = User.objects.get(email=email)
        req = simplejson.load(request)
        nickname = req['nickname']
        user.nickname = nickname
        user.save()
        return SimpleResponse.success_json_response

    return SimpleResponse.post_only(request, change_nickname_function, True)


@csrf_exempt
def change_progress(request):
    """
    修改昵称

    Parameters:
        :request: 指向'/api/change-progress'的POST请求,需要服务器保存session信息(已登录)才能访问\n

    Returns:
        JsonResponse:\n
        :'status': 修改失败'0',修改成功'1'\n
    """
    def change_nickname_function(request, email):
        user = User.objects.get(email=email)
        req = simplejson.load(request)
        progress = int(req['progress'])
        user.game_progress = progress
        user.save()
        return SimpleResponse.success_json_response

    return SimpleResponse.post_only(request, change_nickname_function, True)
