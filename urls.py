from django.urls import path, include
from .import views
from .views import EmpAPIviewset
#from .views import *
from rest_framework.routers import DefaultRouter
from . import views
from django.shortcuts import redirect



router = DefaultRouter()
router.register('Mevaemprec', views.EmpAPIviewset, basename='Mevaemprec')
#router.register('Departmentviewset', views.Departmentviewset, basename='Departmentviewset')

router.register('Skillviewset', views.Skillviewset, basename='Skillviewset')

router.register('Trainingviewset', views.Trainingviewset, basename='Trainingviewset')

router.register('EmployeeSkillviewset', views.EmployeeSkillviewset, basename='EmployeeSkillviewset')

router.register('JobRequirementviewset', views.JobRequirementviewset, basename='JobRequirementviewset')

router.register('Trainingneedviewset', views.Trainingneedviewset, basename='Trainingneedviewset')


router.register('departments', views.Departmentviewset, basename='department')

router.register('RegisterViewSet', views.RegisterViewSet, basename='RegisterViewSet')


from .views import LoginView
from .views import LogoutView
from .views import CurrentUserView


#if i want to open a default router path then i would use this
# def redirect_to_skillviewset(request):
#     return redirect('/Skillviewset/')

urlpatterns = [
    
    path('current-user/', CurrentUserView.as_view(), name='current-user'),
    path('', views.home, name = 'home'),
     #path('', redirect_to_skillviewset, name='redirect-to-skillviewset'),  
     #path('', include(router.urls)),
     
     path('api/', include(router.urls)),
     
     path('login/', LoginView.as_view(), name='login'),
     
     path('logout/', LogoutView.as_view(), name='logout'),
     path('current-user/', CurrentUserView.as_view(), name='current-user'),
     
    
    
 ]