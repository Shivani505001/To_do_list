from django.urls import path 
from .views import TaskList,TaskDetails,TaskCreate,TaskUpdate,TaskDelete,LoginPage,HomeView,Logout,registerpage

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('login/',LoginPage.as_view(),name='login'),
    path('logout',Logout.as_view(),name='logout'),
    path('register/',registerpage.as_view(),name='register'),
    path('tasks/',TaskList.as_view(),name='tasks'),
    path('task/<int:pk>/',TaskDetails.as_view(),name='task'),#pk is default
    #http://127.0.0.1:8000/task/2/ - will display 2nd task
    path('task-create/',TaskCreate.as_view(),name='task-create'),
    path('task-edit/<int:pk>/',TaskUpdate.as_view(),name='task-edit'),
    path('task-del/<int:pk>/',TaskDelete.as_view(),name='task-del'),
    
]
#initially it was from . imort views and 
#views,func_name 
#but now since we r directly importing from views 
#we can directly use TaskList like we used task_list bec now its a class so add as_view() method
#it will trigger a func inside that method 