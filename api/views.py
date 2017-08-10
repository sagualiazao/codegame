from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import simplejson
from api.utils import *
from django.core.mail import send_mail
from api.models import User, DesignedMaps, GameLevels


def get_captcha(request):
    '''
    向web前端发送图片验证码

    Parameters:  
        request - 指向'/api/captcha'的GET请求  
    
    Returns:  
        JsonResponse:  
        'img' - 图片验证码的base64编码  
        'capthca' - 验证码的小写字符串  

    Raises:  
        HTTPResponse('GET please!') - 如果传入请求不是GET
    '''
    if request.method == 'GET':
        img, code = Captcha.base64_captcha()
        # 通过base64编码发送验证码图片
        return JsonResponse({
            'img': img,
            'captcha': code,
        })
    else:
        return HttpResponse('GET please!')

@csrf_exempt
def register(request):
    '''
    执行注册用户操作

    Parameters:  
        request - 指向'/api/register'的POST请求  
    
    Returns:  
        JsonResponse:  
        'status' - 注册失败'0', 注册成功'1'  
        'capthca' - 验证码的小写字符串  

    Raises:  
        HTTPResponse('POST please!') - 如果传入请求不是POST
    '''
    if request.method == 'POST':
        try:
            req = simplejson.load(request)
            email = req['email']
            # 接受到的password是经过前端CBC加密后的字符串
            password_ace = req['password']
            nickname = req['nickname']
            captcha = req['captcha']
            password = CBC.decrypt(captcha, password_ace)
            User.objects.create_user(email=email, nickname=nickname, password=password)
        except BaseException:
            return JsonResponse({ 'status': '0' })
        else:
            return JsonResponse({ 'status': '1' })
    else:
        return HttpResponse('POST please!')

@csrf_exempt
def reset_password_email(request):
    '''
    发送重置密码的邮件验证码

    Parameters:  
        request - 指向'/api/reset-password-email'的POST请求  
    
    Returns:  
        JsonResponse:  
        'status' - 当前邮箱未注册'0', 发送成功'1',发送失败'2'  
        'capthca' - 验证码的小写字符串  

    Raises:  
        HTTPResponse('POST please!') - 如果传入请求不是POST
    '''
    if request.method == 'POST':
        req = simplejson.load(request)
        email = req['email']
        users = User.objects.filter(email=email)
        if len(users) == 0:
            response = JsonResponse({ 'status': '0' })
            return response
        else:
            captcha = ''.join(Captcha.string_captcha())
            msg = '您重置账户: [' + email + '] 密码的验证码是: ' + captcha
            try:
                mail_status = send_mail(
                    r'[验证码]仨瓜俩枣小组的编程游戏-密码重置',
                    msg,
                    'sagualiazao@aliyun.com',
                    [email],
                    fail_silently=False
                    )
            except BaseException:
                return JsonResponse({ 'status': '2' })
            else:
                response = JsonResponse({
                    # 'status': '%s'%mail_status,
                    'status': '1',
                    'captcha': captcha
                })
                return response
    else:
        return HttpResponse('POST please!')

@csrf_exempt
def reset_password(request):
    '''
    重置密码

    Parameters:  
        request - 指向'/api/reset-password'的POST请求  
    
    Returns:  
        JsonResponse:  
        'status' - 修改失败'0', 修改成功'1'  

    Raises:  
        HTTPResponse('POST please!') - 如果传入请求不是POST
    '''
    if request.method == 'POST':
        req = simplejson.load(request)
        email = req['email']
        users = User.objects.filter(email=email)
        if len(users) == 0:
            response = JsonResponse({ 'status': '0' })
            return response
        else:
            try:
                password_ace = req['password']
                captcha = req['captcha']
                password = CBC.decrypt(captcha, password_ace)
                user = users[0]
                user.set_password(password)
                user.save()
            except BaseException:
                return JsonResponse({ 'status': '0' })
            else:
                return JsonResponse({ 'status': '1' })
    else:
        return HttpResponse('POST please!')

@csrf_exempt
def login(request):
    '''
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
    '''
    # POST请求来自主动登录
    if request.method == 'POST':
        req = simplejson.load(request)
        email = req['email']
        users = User.objects.filter(email=email)
        # 用户不存在
        if len(users) == 0:
            response = JsonResponse({ 'status': '0'})
            return response
        else:
            try:
                password_ace = req['password']
                captcha = req['captcha']
                password = CBC.decrypt(captcha, password_ace)
                user = users[0]
                login_status = user.check_password(password)
            except BaseException:
                return JsonResponse({ 'status': '0' })
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
                    return JsonResponse({ 'status': '0'})
    # GET请求来自登录状态检测
    elif request.method == 'GET':
        email = request.session.get('email', False)
        if email == False:
            return JsonResponse({ 'status': '0' })
        else:
            users = User.objects.filter(email=email)
            if len(users) == 0:
                return JsonResponse({ 'status': '0' })
            else:
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
        return HttpResponse('POST or GET plesase!')

def check_email(request):
    '''
    建议邮箱是否已被注册

    Parameters:  
        request - 指向'/api/check-email'的POST请求或GET请求
    
    Returns:  
        JsonResponse:  
        'status' - 未被注册'0', 已被注册'1'  
    '''
    email = request.GET['email']
    users = User.objects.filter(email=email)
    if len(users) == 0:
        return JsonResponse({ 'status': '0' })
    else:
        return JsonResponse({ 'status': '1' })

def logout(request):
    '''
    注销

    Parameters:  
        request - 指向'/api/logout'的GET请求
    
    Returns:  
        JsonResponse:  
        'status' - 注销失败'0', 注销成功'1'  
    '''
    # POST请求来自主动登录
    if request.method == 'GET':
        email = request.session.get('email', False)
        if email == False:
            return JsonResponse({ 'status': '0' })
        else:
            del request.session['email']
            return JsonResponse({ 'status': '1' })
        
@csrf_exempt
def save_map(request):
    '''
    保存关卡地图

    Parameters:  
        request - 指向'/api/save-map'的POST请求
    
    Returns:  
        JsonResponse:  
        'status' - 保存失败'0', 保存成功'1'  
    '''
    # TODO: 增加具体信息的设置
    if request.method == 'POST':
        req = simplejson.load(request)
        map_str = req['mapString']
        try:
            newMap = GameLevels(
                map=map_str,
                level_three_steps=10,
                level_two_steps=20,
                tips='The Level!',
                goal='I donnot know!'
            )
            newMap.save()
        except BaseException:
            return JsonResponse({ 'status': '0' })
        else:
            return JsonResponse({ 'status': '1' })
    elif request.method == 'GET':
        return HttpResponse('POST please!')

@csrf_exempt
def read_map(request):
    '''
    读取关卡地图

    Parameters:  
        request - 指向'/api/read-map'的GET请求
        mapid - 要读取的map的id
    
    Returns:  
        JsonResponse:  
        'status' - 读取失败'0', 读取成功'1'  
        'map' - 地图字符串  
        'threeStar' - 三星评价条件  
        'twoStar' - 两星评价条件  
        'tips' - 关卡提示  
        'goal' - 关卡目标
    '''
    # TODO: 增加具体信息的设置
    if request.method == 'GET':
        map_id = request.GET['mapid']
        selected_map = GameLevels.objects.filter(map_id=map_id)
        if len(selected_map) == 0:
            return JsonResponse({ 'status': '0' })
        else:
            selected_map = selected_map[0]
            return JsonResponse({
                'status': '1',
                'map': selected_map.map,
                'threeStar': selected_map.level_three_steps,
                'twoStar': selected_map.level_two_steps,
                'tips': selected_map.tips,
                'goal': selected_map.goal
            })
    else:
        return HttpResponse('GET please!')