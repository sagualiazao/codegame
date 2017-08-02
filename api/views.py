from django.shortcuts import render
from django.http import HttpResponse
from . import captcha
from io import BytesIO

def get_captcha(request):
    f = BytesIO()
    img, code = captcha.generate_captcha()
    # 将验证码存在服务器的session中，用于校验
    request.session['captcha'] = code
    img.save(f,'PNG')
    return HttpResponse(f.getvalue())
