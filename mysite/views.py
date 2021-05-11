from django.shortcuts import render, redirect
import json
import urllib
from django.conf import settings
from . import models, forms
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.sessions.models import Session
# Create your views here.
# def index(request):
#     years = range(1960,2021)
#     try:
#         urid = request.GET['user_id']
#         urpass = request.GET['user_pass']
#         uryear = request.GET['byear']
#         urfcolor = request.GET.getlist('fcolor')
#     except:
#         urid = None

#     if urid != None and urpass == '12345':
#         verified = True
#     else:
#         verifeid = False
#     return render(request, 'index.html', locals())

def index(request, pid=None, del_pass=None):
    if 'username' in request.session:
        username = request.session['username']
        useremail = request.session['useremail']

    return render(request, 'index.html', locals())


def login(request):
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            login_name = request.POST['username'].strip()
            login_password = request.POST['password']
            try:
                user = models.User.objects.get(name=login_name)
                if user.password == login_password:
                    request.session['username'] = user.name
                    request.session['useremail'] = user.email
                    return redirect('/')
                else:
                    message = "密碼錯誤，請再檢查一次"
            except:
                message = "找不到使用者"
        else:
            message = "請檢查輸入的欄位內容"
    else:
        login_form = forms.LoginForm()

    return render(request, 'login.html', locals())


def logout(request):
    if 'username' in request.session:
        Session.objects.all().delete()
        return redirect('/login/')
    return redirect('/')


def listing(request):
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:150]
    moods = models.Mood.objects.all()
    return render(request, 'listing.html', locals())


def posting(request):
    moods = models.Mood.objects.all()
    message = '如要張貼訊息，則每一個欄位都要填...'
    return render(request, 'posting.html', locals())


def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            message = "感謝您的來信。"
            user_name = form.cleaned_data['user_name']
            user_city = form.cleaned_data['user_city']
            user_school = form.cleaned_data['user_school']
            user_email  = form.cleaned_data['user_email']
            user_message = form.cleaned_data['user_message']
            mail_body = u'''
網友姓名：{}
居住城市：{}
是否在學：{}
反應意見：如下
{}'''.format(user_name, user_city, user_school, user_message)
            send_mail(
    '不吐不快',
    mail_body,
    'a6898208@gmail.com',
    [user_email],
    fail_silently=False,
)

        else:
            message = "請檢查您輸入的資訊是否正確！"
    else:
        form = forms.ContactForm()
    return render(request, 'contact.html', locals())



def post2db(request):
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''
            if result['success']:
                message = "您的訊息已儲存，要等管理者啟用後才看得到喔。"
                post_form.save()
                return HttpResponseRedirect('/list/')
            else:
                message = "Invalid reCAPTCHA. Please try again."
        else:
            message = '如要張貼訊息，則每一個欄位都要填...'
    else:
        post_form = forms.PostForm()
        message = '如要張貼訊息，則每一個欄位都要填...'          

    return render(request, 'post2db.html', locals())


def userinfo(request):
    if 'username' in request.session:
        username = request.session['username']
    else:
        return redirect('/login/')

    try:
        userinfo = models.User.objects.get(name=username)
    except:
        pass

    return render(request, 'userinfo.html', locals())