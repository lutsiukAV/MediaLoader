"""MediaLoader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from media_saver import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^signup/', views.sign_up),
    url(r'^login/', views.sign_in),
    url(r'^logout/', views.out),
    url(r'^addMedia/', views.addMedia),
    url(r'^getMedia/', views.getMedia),
    url(r'^load/', views.loadInfo),
    url(r'^editMedia/', views.editMedia),
    url(r'^instagramlog/', views.instalog),
    url(r'^getInstaMedia/', views.getInstaMedia),
    url(r'^listView/', views.list_view),
    url(r'^addInstaMedia/', views.addInstaMedia),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
