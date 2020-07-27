from django.urls import path
from .views import GetMensajes,GetMensaje,CreateMensaje,UpdateMensaje,DeleteMensaje

app_name='mensajes'
urlpatterns = [
    path('', GetMensajes, name='list'),
    path('<int:id>',GetMensaje,name="detail"),
    path('create/',CreateMensaje.as_view(),name="create"),
    path('update/<int:id>/',UpdateMensaje.as_view(),name="update"),
    path('delete/<int:id>/',DeleteMensaje,name ="delete")
]