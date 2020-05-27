import random
from io import BytesIO

from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from PIL import Image, ImageDraw, ImageFont
from django.contrib import auth

from app01 import models
from app01.bbsform import RegForm
# Create your views here.

#登录
def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.is_ajax():
    # elif request.method == "POST":
        response = {'code': 100, 'msg': None}
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        code = request.POST.get('code')
        print(name, pwd)
        if request.session['valid_code'].upper() == code.upper():
            user = auth.authenticate(request, username=name, password=pwd)
            if user:
                response['msg'] = "登录成功"
                #在后续的视图函数中直接request.user可以取到当前登录用户
                auth.login(request, user)

            else:
                response['code'] = 101
                response['msg'] = "用户名或密码错误"
        else:
            response['code'] = 102
            response['msg'] = "验证码错误"
        return JsonResponse(response)
#获取随机颜色
def get_random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
#获取验证码
def get_code(request):
    # # 方式一，返回固定图片
    #  with open("static/image/code.jpg", 'rb') as f:
    #     data = f.read()
    # return HttpResponse(data)

    # # 方式二，自动生成图片，需要借助第三方模块pillow
    # img = Image.new('RGB', (300, 40), get_random_color())
    # #把图片保存
    # with open("static/image/code.jpg", 'wb')as f:
    #     img.save(f)
    # #打开返回
    # with open("static/image/code.jpg", 'rb') as f:
    #     data = f.read()
    # return HttpResponse(data)

    # #方式三（不把文件保存在硬盘上，以Bytes格式保存在内存中)
    # #新生成一张图片
    # img = Image.new('RGB', (300, 40), get_random_color())
    # #写文字
    # draw = ImageDraw.Draw(img)
    # #生成一个字体对象
    # font = ImageFont.truetype("static/font/msjh_console.ttf", 34)
    # draw.text((0,10), "python", font=font)
    # #生成一个ByteIO对象
    # f = BytesIO()
    # #把文件保存在对象中
    # img.save(f, 'png')
    # # f.getvalue()把文件从对象中取出来
    # return HttpResponse(f.getvalue())
    #应用版
    valid_code = ''
    img = Image.new('RGB', (300, 45), get_random_color())
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("static/font/msyh_boot.ttf", 34)
    #动态生成五个大小写、数字
    for i in range(5):
        num = str(random.randint(0, 9))
        up_char = str(chr(random.randint(65, 90)))
        lower_char = str(chr(random.randint(97, 122)))
        choice_char = random.choice([num, up_char, lower_char])
        valid_code += choice_char
        draw.text((20+i*50, 5), choice_char, font=font)
    print(valid_code)
    request.session['valid_code'] = valid_code
    # #画点、线、弧
    # width = 320
    # height = 35
    # for i in range(10):
    #     x1 = random.randint(0, width)
    #     y1 = random.randint(0, width)
    #     x2 = random.randint(0, height)
    #     y2 = random.randint(0, height)
    #     #在图片上画线
    #     draw.line((x1, y1, x2, y2), fill=get_random_color())
    # for i in range(100):
    #     #画点
    #     draw.point([random.randint(0, width), random.randint(0, height)])
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     #画弧形
    #     draw.arc((x, y, x+4, y+4), 0, 90, fill=get_random_color())
    f = BytesIO()
    img.save(f, 'png')
    return HttpResponse(f.getvalue())
#注册
def register(request):
    if request.method=="GET":
        form = RegForm()
        return render(request, 'register.html', {"form":form})
    elif request.is_ajax():
        response = {'code':100,'msg':None}
        form = RegForm(request.POST)
        if form.is_valid():
            #校验通过的数据
            clean_data = form.cleaned_data
            #剔除多余数据re_pwd
            clean_data.pop('re_pwd')
            #取出头像
            avatar = request.FILES.get('avatar')
            if avatar:
                #models中是FileField,只需要把文件对象赋值给avater字段，自动保存
                clean_data['avatar'] = avatar
            user = models.UserInfo.objects.create_user(**clean_data)
            if user:
                response['msg'] = "注册成功"
                auth.login(request, user)

            else:
                response['code'] = 103
                response['msg'] = "创建失败"
        else:
            response['code'] = 101
            #把错误信息返回显示
            response['msg'] = form.errors
        return JsonResponse(response, safe=False)
#首页
def index(request):
    article_list = models.Article.objects.all()
    return render(request, 'index.html', {"article_list": article_list})
#退出
def logout(requset):
    auth.logout(requset)
    return redirect("/app01/index/")
#个人站点
def site(request, username, *args, **kwargs):
    print(args)
    print(kwargs)
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request, "error.html")
    else:
        #查出用户的所有文章:根据用户得到个人站点-->取个人站点的所有文章
        blog = user.blog
        article_list = blog.article_set.all()
    #过滤
    condition = kwargs.get('condition')
    params = kwargs.get('params')
    if condition == 'tag':
        article_list = article_list.filter(tag=params)
    elif condition == 'category':
        article_list = article_list.filter(category=params)
    elif condition == 'archive':
        year_month = params.split('-')
        article_list = article_list.filter(create_time__year=year_month[0], create_time__month=year_month[1])

    #查询个人站点所有分类对应的文章数
    category_ret = models.Category.objects.all().filter(blog=blog).values('nid').annotate(cou=Count('article__nid')).values_list('title', 'cou', 'nid')
    print(category_ret)
    #查询个人站点所有标签对应的文章数
    tag_ret = models.Tag.objects.all().filter(blog=blog).annotate(cou=Count('article__nid')).values_list('title', 'cou', 'nid')
    print(tag_ret)
    #查询年月对应的文章数
    year_ret = models.Article.objects.annotate(month=TruncMonth('create_time')).values('month').annotate(cou=Count('nid')).values_list('month', 'cou')
    print(year_ret)
    return render(request, 'site.html', locals())

def article_detail(request, username, id):
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request, "error.html")
    else:
        blog = user.blog
    category_ret = models.Category.objects.all().filter(blog=blog).values('nid').annotate(cou=Count('article__nid')).values_list('title', 'cou', 'nid')
    tag_ret = models.Tag.objects.all().filter(blog=blog).annotate(cou=Count('article__nid')).values_list('title', 'cou', 'nid')
    year_ret = models.Article.objects.annotate(month=TruncMonth('create_time')).values('month').annotate(cou=Count('nid')).values_list('month', 'cou')
    article = models.Article.objects.filter(nid=id).first()

    return render(request, 'article_detail.html', locals())