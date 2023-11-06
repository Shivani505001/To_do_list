from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
#from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView,UpdateView,FormView,DeleteView
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 


from .models import task
import datetime



# Create your views here.

class HomeView(View):
    template_name = 'base/home.html'

    def get_context_data(self):
        context = {
            'app_name': 'To do List',
            'current_date': datetime.date.today(),
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

class LoginPage(LoginView):
    template_name = 'base/login.html'
    fields='__all__'
    redirect_authenticated_user = True #so that after logging in user can't go back to login page
    def get_success_url(self) :
        return reverse_lazy('tasks')

class registerpage(FormView):
    form_class= UserCreationForm
    template_name='base/register.html'
    redirect_authenticated_user = True #this should not allow the authenticated user to get back to this page
    success_url=reverse_lazy('tasks')
    
    def form_valid(self, form) : #This method is called when a valid form is submitted
        user=form.save() #saves the data of the new user who registered 
        if user is not None: #ie if the user is registration over and is not none then login this user 
            login(self.request,user)#login() isna built in fun used to authenticated the user and create a session for them 
        return super(registerpage,self).form_valid(form) #using super(registerpage, self) to call the form_valid method from the parent class of registerpage.
#registerpage is name of the class in parent class

#return super(registerpage, self).form_valid(form) is using the super() function to call the form_valid method from the parent class of registerpage. 
# It passes the form argument to this method. This is a common pattern in class-based views when you want to extend the behavior 
# of a method from a parent class while preserving some of the functionality of that method.
    def get(self, *args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(registerpage,self).get(*args,**kwargs)
#even after using redirect_authenticated_user = True I can still go to register page after logging in so I manually 
#made the function so that once user is authenticated they can't go back to register page.
class Logout(LogoutView):
    next_page='home'

    
class TaskList(LoginRequiredMixin, ListView):
    model = task
    context_object_name='tasks'
    # def get_queryset(self):
    #     # Filter tasks based on the current user
    #     return task.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs) : #I used this method so that each user can see their list of tasks onli
        context=super().get_context_data(**kwargs)
        # context['tasks']=super().get_context_data(**kwargs) 
        # print("Before filtering:", context['tasks'])
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        # print("After filtering:", context['tasks'])
        context['count']=context['tasks'].filter(complete=False).count()
        
        search_input=self.request.GET.get('search_area') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(
                title__icontains=search_input)
        context['search_input']=search_input
        return context

class TaskDetails(LoginRequiredMixin, DetailView):
    model=task
    context_object_name= 'task'
    template_name= 'base/task.html'
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model=task
    fields=['title','description','complete'] #creates a form with mentioned felids - creating form is possible in CreateView
    success_url = reverse_lazy('tasks')
    # template_name ='base/create.html'
    context_object_name= 'task-create'
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model=task 
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')
    # template_name ='base/create.html'

class TaskDelete(LoginRequiredMixin, DeleteView):
    model=task
    feilds='__all__'
    success_url=reverse_lazy('tasks')
    template_name ='base/delete.html'