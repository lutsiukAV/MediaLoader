from django.shortcuts import render
from django.http import HttpResponse
from media_saver.models import Media, User, SocialAccount
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
import requests
import json
import datetime

def index(request):
    return HttpResponse(render(request, 'index.html'))

def sign_up(request):
    if request.method == 'POST':
        users = User.objects.filter(username=request.POST['login'])
        if len(users) == 0:
            u = User.objects.create_user(username=request.POST['login'], password = request.POST['password'])
            u.save()
        else:
            HttpResponse(render(request, 'index.html', context={'message': "Login exists"}))
        return HttpResponse(render(request, 'login.html'))

def groupMedia(media):
    media_in_row = 4
    result = []
    current = []
    for i in range(len(media)):
        if i > 0 and i % media_in_row == 0:
            result.append(current)
            current = []
        current.append(media[i])
    if len(current) > 0:
        result.append(current)
    print(result)
    return result

def sign_in(request):
    if request.method == 'GET':
        return HttpResponse(render(request, 'login.html'))
    if request.method == 'POST':
        usr = authenticate(username=request.POST['login'], password=request.POST['password'])
        if usr is not None:
            login(request, usr)
            media = Media.objects.filter(user=usr)
            is_logged = len(SocialAccount.objects.filter(user=usr)) > 0
            row_media = groupMedia(media)
            return HttpResponse(render(request, 'media.html', context={'media': row_media, 'is_logged': is_logged}))
        else:
            return HttpResponse(render(request, 'login.html'))


@login_required(login_url='/login/')
def out(request):
    logout(request)
    return HttpResponse(render(request, 'login.html'))


@ensure_csrf_cookie
@login_required(login_url='/login/')
def getMedia(request):
    u = User.objects.get(id=request.user.id)
    is_logged = len(SocialAccount.objects.filter(user=u)) > 0
    media = Media.objects.filter(user=u)
    row_media = groupMedia(media)
    return HttpResponse(render(request, 'media.html', context={'media': row_media, 'is_logged': is_logged}))

@ensure_csrf_cookie
@login_required(login_url='/login/')
def list_view(request):
    u = User.objects.get(id=request.user.id)
    is_logged = len(SocialAccount.objects.filter(user=u)) > 0
    media = Media.objects.filter(user=u)
    return HttpResponse(render(request, 'list_view.html', context={'media': media, 'is_logged': is_logged}))

@ensure_csrf_cookie
@login_required(login_url='/login/')
def addMedia(request):
    usr = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        if 'file' in request.FILES:
            img = request.FILES['file']
            title = request.POST['title']
            description = request.POST['description']
            date = str(request.POST['date'])
            if request.POST["media_type"] == "Photo":
                media = Media.objects.create(user=usr, image=img, title=title, description=description,
                                             date=date, mtype=0)
            else:
                media = Media.objects.create(user=usr, file=img, title=title, description=description,
                                             date=date, mtype=1)
            media.save()
            m = Media.objects.filter(user=usr)
            is_logged = len(SocialAccount.objects.filter(user=usr)) > 0
            row_media = groupMedia(m)
            return HttpResponse(render(request, 'media.html', context={'media': row_media, 'is_logged': is_logged}))
        url = request.POST['url']
        title = request.POST['title']
        description = request.POST['description']
        date = str(request.POST['date'])
        if request.POST["media_type"] == "Photo":
            media = Media.objects.create(user=usr, url=url, title=title, description=description, date=date, mtype=0)
        else:
            media = Media.objects.create(user=usr, url=url, title=title, description=description, date=date, mtype=1)
        media.save()
        m = Media.objects.filter(user=usr)
        is_logged = len(SocialAccount.objects.filter(user=usr)) > 0
        row_media = groupMedia(m)
        return HttpResponse(render(request, 'media.html', context={'media': row_media, 'is_logged': is_logged}))


@ensure_csrf_cookie
@login_required(login_url='/login/')
def loadInfo(request):
    media = Media.objects.get(id=request.GET['id'])
    return HttpResponse(render(request, 'info.html', context={'media': media}))

@ensure_csrf_cookie
@login_required(login_url='/login/')
def editMedia(request):
    media = Media.objects.get(id=request.POST['id'])
    media.title = request.POST['title']
    media.description = request.POST['description']
    media.date = str(request.POST['date'])
    media.save()
    u = User.objects.get(id=request.user.id)
    is_logged = len(SocialAccount.objects.filter(user=u)) > 0
    m = Media.objects.filter(user=u)
    row_media = groupMedia(m)
    return HttpResponse(render(request, 'media.html', context={'media': row_media, 'is_logged': is_logged}))

@login_required(login_url='/login/')
def instalog(request):
    code = request.GET['code']
    r = requests.post('https://api.instagram.com/oauth/access_token', data={'client_id': 'd72fed8e31384a159c5221297d2579fe', 'client_secret': '795b87d670d74556b6f8607e96666b6a', 'grant_type': 'authorization_code', 'redirect_uri': 'http://127.0.0.1:8000/instagramlog', 'code': code})
    print(r.text)
    access_token = json.loads(r.text)['access_token']
    account = SocialAccount.objects.create(instagram=access_token, user=request.user)
    account.save()
    u = User.objects.get(id=request.user.id)
    is_logged = len(SocialAccount.objects.filter(user=u)) > 0
    media = Media.objects.filter(user=u)
    row_media = groupMedia(media)
    return HttpResponse(render(request, 'media.html', context={'media': row_media, 'is_logged': is_logged}))

@login_required(login_url='/login/')
def getInstaMedia(request):
    access_token = SocialAccount.objects.get(user=request.user).instagram
    r = requests.get('https://api.instagram.com/v1/users/self/media/recent/?access_token=' + access_token, params={'ACCESS_TOKEN': access_token})
    if r.status_code == 400:
        u = User.objects.get(id=request.user.id)
        SocialAccount.objects.filter(user=u).delete()
        is_logged = len(SocialAccount.objects.filter(user=u)) > 0
        media = Media.objects.filter(user=u)
        row_media = groupMedia(media)
        return HttpResponse(render(request, 'media.html', context={'media': row_media, 'is_logged': is_logged}))
    else:
        instagram_media = []
        current = []
        data = json.loads(r.text)['data']
        for d in data:
            url = d['images']['standard_resolution']['url']
            date = d['caption']['created_time']
            title = d['caption']['text']
            current.append(url)
            current.append(datetime.datetime.fromtimestamp(float(date)))
            current.append(title)
            instagram_media.append(current)
            current = []
        return HttpResponse(render(request, 'instalog.html', context={'media': instagram_media}))

@login_required(login_url='/login')
def addInstaMedia(request):
    url = request.GET['url']
    date = request.GET['date']
    title = request.GET['title']
    user = request.user
    insta_media = Media.objects.create(user=user, url=url, title=title, description=title, date=str(date), mtype=0)
    insta_media.save()
    is_logged = len(SocialAccount.objects.filter(user=user)) > 0
    m = Media.objects.filter(user=user)
    row_media = groupMedia(m)
    return HttpResponse(render(request, 'media.html', context={'media': row_media, 'is_logged': is_logged}))



