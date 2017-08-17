from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
import simplejson
from api.utils import *
from django.core.mail import send_mail
from api.models import User, DesignedMaps, GameLevels


def get_captcha(request):
    """
    向web前端发送图片验证码

    Parameters:  
        request - 指向'/api/captcha'的GET请求  
    
    Returns:  
        JsonResponse:  
        'img' - 图片验证码的base64编码  
        'capthca' - 验证码的小写字符串  

    Raises:  
        HTTPResponse('GET please!') - 如果传入请求不是GET
    """
    if request.method == 'GET':
        img, code = Captcha.base64_captcha()
        # 通过base64编码发送验证码图片
        return JsonResponse({
            'img': img,
            'captcha': code,
        })
    else:
        return HttpResponseNotFound()


@csrf_exempt
def register(request):
    """
    执行注册用户操作

    Parameters:  
        request - 指向'/api/register'的POST请求  
    
    Returns:  
        JsonResponse:  
        'status' - 注册失败'0', 注册成功'1'  
        'capthca' - 验证码的小写字符串  

    Raises:  
        HTTPResponse('POST please!') - 如果传入请求不是POST
    """
    if request.method == 'POST':
        try:
            # 捕获json为空的错误
            req = simplejson.load(request)
            email = req['email']
            # 邮件格式错误返回
            if check_email_format(email) == False:
                return JsonResponse({'status': '0'})
            # 账户已存在返回
            if len(User.objects.filter(email=email)) > 0:
                return JsonResponse({'status': '0'})
            # 捕获其他值为空的错误
            password_ace = req['password']
            nickname = req['nickname']
            captcha = req['captcha']
            # 捕获密码编码错误
            password = CBC.decrypt(captcha, password_ace)
            User.objects.create_user(email=email, nickname=nickname, password=password)
        except BaseException:
            return JsonResponse({'status': '0'})
        else:
            return JsonResponse({'status': '1'})
    else:
        return HttpResponseNotFound()


@csrf_exempt
def reset_password_email(request):
    """
    发送重置密码的邮件验证码

    Parameters:  
        request - 指向'/api/reset-password-email'的POST请求  
    
    Returns:  
        JsonResponse:  
        'status' - 发送失败'0', 发送成功'1'  
        'capthca' - 验证码的小写字符串  

    Raises:  
        HTTPResponse('POST please!') - 如果传入请求不是POST
    """
    if request.method == 'POST':
        try:
            # 捕获json为空错误
            req = simplejson.load(request)
            email = req['email']
            users = User.objects.filter(email=email)
            # 如果该用户不存在,不需要再检查格式错误
            if len(users) == 0:
                return JsonResponse({'status': '0'})
            # 用户存在,发送验证邮件
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
        except BaseException:
            return JsonResponse({'status': '0'})
        return JsonResponse({'status': '1'})
    else:
        return HttpResponseNotFound()


def check_email_captcha(request):
    """
    建议输入的邮件验证码是否正确

    Parameters:  
        request - 指向'/api/check-email'的POST请求或GET请求
    
    Returns:  
        JsonResponse:  
        'status' - 未被注册'0', 已被注册'1'  
    """
    if request.method == 'GET':
        try:
            captcha = request.GET['captcha']
            if captcha != request.session['captcha']:
                return JsonResponse({'status': '0'})
            else:
                return JsonResponse({'status': '1'})
        except BaseException:
            return JsonResponse({'status': '0'})
    else:
        return HttpResponseNotFound()


@csrf_exempt
def reset_password(request):
    """
    重置密码

    Parameters:  
        request - 指向'/api/reset-password'的POST请求  
    
    Returns:  
        JsonResponse:  
        'status' - 修改失败'0', 修改成功'1'  

    Raises:  
        HTTPResponse('POST please!') - 如果传入请求不是POST
    """
    if request.method == 'POST':
        try:
            # 捕获json为空错误
            req = simplejson.load(request)
            email = req['email']
            users = User.objects.filter(email=email)
            # 如果该用户不存在,不需要检查邮箱格式
            if len(users) == 0:
                return JsonResponse({'status': '0'})
            # 捕获值缺少或错误
            password_ace = req['password']
            captcha = req['captcha']
            password = CBC.decrypt(captcha, password_ace)
            user = users[0]
            user.set_password(password)
            user.save()
        except BaseException:
            return JsonResponse({'status': '0'})
        return JsonResponse({'status': '1'})
    else:
        return HttpResponseNotFound()


@csrf_exempt
def login(request):
    """
    登录

    Parameters:  
        request - 指向'/api/login'的POST请求或GET请求
    
    Returns:  
        JsonResponse:  
        'status' - 登录失败'0', 登录成功'1'  
        'email' - 用户的电子邮件  
        'nickname' - 用户的昵称  
        'id' - 用户的id
        'gameProgress' - 用户的游戏进度
        'hasPaied' - 用户是否已经付费
    """
    # POST请求来自主动登录
    if request.method == 'POST':
        try:
            # 捕获json为空错误
            req = simplejson.load(request)
            email = req['email']
            users = User.objects.filter(email=email)
            # 用户不存在,不需要检查邮箱格式
            if len(users) == 0:
                return JsonResponse({'status': '0'})
            # 捕获信息不全错误
            password_ace = req['password']
            captcha = req['captcha']
            password = CBC.decrypt(captcha, password_ace)
            user = users[0]
            login_status = user.check_password(password)
        except BaseException:
            return JsonResponse({'status': '0'})
        else:
            # 登录成功
            if login_status:
                # 设置session的用户邮箱字段
                request.session['email'] = email
                return JsonResponse({
                    'status': '1',
                    'email': user.email,
                    'nickname': user.nickname,
                    'id': user.id,
                    'gameProgress': user.game_progress,
                    'hasPaied': user.has_paied,
                    'createdAt': user.created_at
                })
            else:
                return JsonResponse({'status': '0'})
    # GET请求来自登录状态检测
    elif request.method == 'GET':
        email = request.session.get('email', False)
        if email == False:
            return JsonResponse({'status': '0'})
        else:
            users = User.objects.filter(email=email)
            user = users[0]
            return JsonResponse({
                'status': '1',
                'email': user.email,
                'nickname': user.nickname,
                'id': user.id,
                'gameProgress': user.game_progress,
                'hasPaied': user.has_paied,
                'createdAt': user.created_at
            })
    else:
        return HttpResponseNotFound()


def check_email(request):
    """
    检验邮箱是否已被注册

    Parameters:  
        request - 指向'/api/check-email'的POST请求或GET请求
    
    Returns:  
        JsonResponse:  
        'status' - 未被注册'0', 已被注册'1'  
    """
    if request.method == 'GET':
        try:
            email = request.GET['email']
            users = User.objects.filter(email=email)
        except BaseException:
            return JsonResponse({'status': '0'})
        else:
            if len(users) == 0:
                return JsonResponse({'status': '0'})
            else:
                return JsonResponse({'status': '1'})
    else:
        return HttpResponseNotFound()

def logout(request):
    """
    注销

    Parameters:  
        request - 指向'/api/logout'的GET请求
    
    Returns:  
        JsonResponse:  
        'status' - 注销失败'0', 注销成功'1'  
    """
    # POST请求来自主动登录
    if request.method == 'GET':
        email = request.session.get('email', False)
        if email == False:
            return JsonResponse({'status': '0'})
        else:
            del request.session['email']
            return JsonResponse({'status': '1'})
    else:
        return HttpResponseNotFound()

@csrf_exempt
def save_map(request):
    """
    保存用户编辑的地图

    Parameters:  
        request - 指向'/api/save-map'的POST请求
        mapString - 要存储的地图信息  
        name - 地图的名称  
        remarks - 地图的说明  
    
    Returns:  
        JsonResponse:  
        'status' - 保存失败'0', 保存成功'1'  
    """
    # TODO: 增加具体信息的设置
    if request.method == 'POST':
        try:
            # 捕获json为空错误
            req = simplejson.load(request)
            # 捕获参数错误
            email = request.session['email']
            author = User.objects.get(email=email)
            map_str = req['mapString']
            name = req['name']
            remarks = req['remarks']
            newMap = DesignedMaps(
                map=map_str,
                name=name,
                remarks=remarks,
                author=author,
                is_published=False
            )
            newMap.save()
            status = MapImage.generate_map_image(newMap.map_id, map_str)
        except BaseException:
            return JsonResponse({'status': '0'})
        else:
            return JsonResponse({'status': '1'})
    else:
        return HttpResponseNotFound()


@csrf_exempt
def read_map(request):
    """
    读取用户编辑的地图

    Parameters:  
        request - 指向'/api/read-map'的GET请求
        mapid - 要读取的map的id
    
    Returns:  
        JsonResponse:  
        'status' - 读取失败'0', 读取成功'1'  
        'map' - 地图字符串  
        'name' - 地图名  
        'remarks' - 地图说明  
        'author' - 地图作者  
        'is_published' - 地图发布状态
    """
    # TODO: 增加具体信息的设置
    if request.method == 'GET':
        try:
            map_id = int(request.GET['mapid'])
            selected_map = DesignedMaps.objects.filter(map_id=map_id)
            if len(selected_map) == 0:
                return JsonResponse({'status': '0'})
            else:
                selected_map = selected_map[0]
                return JsonResponse({
                    'status': '1',
                    'map': selected_map.map,
                    'name': selected_map.name,
                    'remarks': selected_map.remarks,
                    'author': str(selected_map.author)
                })
        except BaseException as e:
            return JsonResponse({'status': '0'})
    else:
        return HttpResponseNotFound()
