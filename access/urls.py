from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.static import serve 


urlpatterns = [ 
    path('home/',views.home,name='home'),
    path('dash/',views.dash,name='dash'),
    path('about/',views.about,name='about'),
    path('plan/',views.plan,name='plan'),
    path('faq/',views.faq,name='faq'),
    path('assets_recovery/',views.assets_recovery,name='assets_recovery'),
    path('contact/',views.contact,name='contact'),
    path('signup/',views.signup_view,name='signup'),
    path('login/',views.login_view,name='login'),
    path('profile/',views.profile_view,name='profile'),
    path('referals/',views.referals,name='referals'),
    path('Deposit/',views.Deposit_view,name='Deposit'),
    path('Deposit_his/',views.Deposit_his_view,name='Deposit_his'),
    path('purchase_plan/',views.purchase_plan,name='purchase_plan'),
    path('view_plans/',views.view_plans,name='view_plans'),
    path('withdraw/',views.withdraw_view,name='withdraw'),
    path('withdraw_history/',views.withdraw_history_view,name='withdraw_history'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



 

