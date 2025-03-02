from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.static import serve 


urlpatterns = [ 
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('plan/',views.plan,name='plan'),
    path('faq/',views.faq,name='faq'),
    path('assets_recovery/',views.assets_recovery,name='assets_recovery'),
    path('contact/',views.contact,name='contact'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



 

