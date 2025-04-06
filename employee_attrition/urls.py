from django.urls import path
from .views import predict_attrition, home#, index
from .views import home_page, about_page, service_page, project_page

urlpatterns = [
    path('', home_page, name='home'),  # Home page at the root URL
    path('about/', about_page, name='about'),
    path('service/', service_page, name='service'),
    path('project/', project_page, name='project'),
    #path('index/', index, name='index'),
    #path('', home, name='home'),
    path('predict/', predict_attrition, name='predict_attrition'),
]


