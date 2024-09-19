

from django.contrib import admin

from .models import EmployeeDetails
from django.contrib.auth.models import User

from .models import *


#from authentication.models import User



class ProjectAdmin(admin.ModelAdmin):
    list_display =('first_name', 'id', 'last_name', 'employee_id', 'start_date', 'status', 'created_at')
    list_editable = ('first_name', 'last_name')
    list_display_links = ('id', 'status')
    ordering= ('-id',)
    #readonly_fields = ('email', 'password',) to make fields uneditable
    #note you cannot add a many to many field in a list_display like the departments
   
    
  

class SkillAdmin(admin.ModelAdmin):
    list_display =('name', 'created_at', 'modified_at')
    
admin.site.register(Department)

admin.site.register(EmployeeDetails, ProjectAdmin)
admin.site.register(Training)
admin.site.register(EmployeeSkill)
admin.site.register(JobRequirement)
admin.site.register(Skill, SkillAdmin)
admin.site.register(TrainingNeed)




