from django.urls import path
from . import views
urlpatterns=[path('',views.home,name='home'),
path('addcomplaint',views.addcomplaint,name='addcomplaint'),
path('detail',views.detail,name='detail'),
path('detailed/<int:id>',views.detailed,name='detailed'),
path('delete/<int:id>',views.delete,name='delete'),
path('register',views.registerPage,name='register'),
path('login',views.loginPage,name='login'),
path('logout',views.logoutUser,name='logout'),
path('profile',views.profile,name='profile'),
path('feedback/<int:id>',views.feedback,name='feedback'),
path('changestatus/<int:id>',views.changestatus,name='changestatus'),
path('mycomplaint',views.mycomplaint,name='mycomplaint'),
path('reject/<int:id>',views.reject,name='reject'),
path('mydetailed/<int:id>',views.mydetailed,name='mydetailed'),
path('reopen/<int:id>',views.reopen,name='reopen'),
path('pdf/',views.pdf,name='pdf'),
]