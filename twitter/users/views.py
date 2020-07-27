from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django import views
from .forms import UserForm, ProfileForm, UserCreateForm, UserUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from mensajes.models import Mensaje




# Create your views here.



def GetUsers(request):
    users = User.objects.all()
    
    template_name = "users/list.html"
    context = {
        'users': users
    }
    return render(request, template_name, context)

def GetUser(request,id):
    user = User.objects.get(pk=id)
    mensajes =  Mensaje.objects.filter(user=user)
    print(mensajes)
    template_name='users/detail.html'
    context={
    'user' : user,
    'mensajes': mensajes
    }
    return render(request,template_name,context)




def DeleteUser(request,id):
    user = User.objects.get(pk=id)
    user.delete()
    #messages.info(request,'Se elimino usuario')
    return redirect('users:list')



class CreateUser(views.View):
    def get(self,request):
        user_form = UserForm()
        profile_form = ProfileForm()
        template_name = 'users/form.html'
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request,template_name,context)
    def post(self, request):
        user_form = UserCreateForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(request.POST['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('users:detail', user.id)
        else:
            template_name= "users/form.html"
            context = {
                'user_form' : user_form,
                'profile_form' : profile_form
            }
            return render(request,template_name,context)

class UpdateUser(views.View):
    def get(self,request,id):
        user = User.objects.get(pk=id)
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)
        template_name = 'users/form.html'
        context = {
                'user_form' : user_form,
                'profile_form': profile_form,
                'id' : id,
                'image' : user.profile.image
        }
        return render(request,template_name,context)
    
    def post(self,request,id):
        user = User.objects.get(pk=id)
        user_form = UserUpdateForm(request.POST,instance=user)
        profile_form = ProfileForm(request.POST,request.FILES,instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save()
            return redirect('users:detail',id)
        else:
            template_name = 'user_form.html'
        context = {
                'user_form' : user_form,
                'profile_form' : profile_form,
                'id' : id,
                'image': user.profile.image
        }

        return render(request,template_name,context)


class Login(views.View):
    def get(self, request):
        auth_form = AuthenticationForm()
        template_name = 'users/login.html'
        context = {
            'form': auth_form
        }
        return render(request, template_name, context)
    def post(self, request):
        try:
            auth_form = AuthenticationForm(data=request.POST)
            if auth_form.is_valid():
                username = auth_form.cleaned_data['username']
                password = auth_form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    # messages.success(request, 'Inciaste sesión éxito')
                    return redirect('users:detail', user.id)
                else:
                    template_name = 'users/login.html'
                    context = {
                        'form': auth_form
                    }
                    # messages.error(request, 'Credenciales inválidas')
                    return render(request, template_name, context)
            else:
                template_name = 'users/login.html'
                context = {
                    'form': auth_form
                }
                return render(request, template_name, context)
        except Exception as e:
            template_name = 'users/login.html'
            context = {
                'form': auth_form
            }
            # messages.error(request, 'Credenciales inválidas')
            return render(request, template_name, context)


def Logout(request):
    #logout(request)
    #messages.info(request, 'Sesión cerrada con éxito')
    return redirect('login')


def validate_authenticate(request):
    if request.user.is_authenticated:
        return redirect('users:detail', request.user.id)
    else:
        return redirect('login')

