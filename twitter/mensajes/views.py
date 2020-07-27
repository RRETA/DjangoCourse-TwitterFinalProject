from django.shortcuts import render,redirect
from django import views
from .models import Mensaje
from .forms import MensajeForm
from django.contrib.auth.decorators import login_required
# Create your views here.



def GetMensajes(request):
    mensajes = Mensaje.objects.all()
    template_name= 'mensajes/list.html'
    context={
        'mensajes':mensajes
    }
    return render(request,template_name,context)


def GetMensaje(request,id):
    mensaje = Mensaje.objects.get(pk=id)
    template_name='mensajes/detail.html'
    context={
    'mensaje' : mensaje
    }
    return render(request,template_name,context)



class CreateMensaje(views.View):
    def get(self,request):
        form = MensajeForm()
        template_name='mensajes/form.html'
        context= {
            'form':form

        }
        return render(request,template_name,context)

    def post(self, request):
        new_form = MensajeForm(request.POST) 
        if new_form.is_valid():
            new_address = new_form.save()
            return redirect('mensajes:list')
        else:
            template_name = 'mensajes/form.html'
            context = {
                'form': new_form
            }
            return render(request, template_name, context) 


class UpdateMensaje(views.View):
    def get(self, request, id):
        mensaje = Mensaje.objects.get(pk=id)
        form = MensajeForm(instance=mensaje)
        template_name = 'mensajes/form.html'
        context = {
            'form': form,
            'mensaje': mensaje
        }
        return render(request, template_name, context)
    def post(self, request, id):
        mensaje = Mensaje.objects.get(pk=id)
        form_updated = MensajeForm(request.POST, instance=mensaje)
        if form_updated.is_valid():
            form_updated.save()
            return redirect('mensajes:detail', mensaje.id)
        else:
            template_name = 'mensajes/form.html'
            context = {
                'form': form_updated,
                'mensaje': mensaje
            }
            return render(request, template_name, context)


def DeleteMensaje(request, id):
    mensaje = Mensaje.objects.get(pk=id)
    mensaje.delete()
    return redirect('mensajes:list')