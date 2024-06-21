from django.urls import path
from .views import upload_file
from .views import hello_world

urlpatterns = [
    path("", upload_file, name = 'file-upload'),
    path("test/", hello_world, name = 'hello-world')
]