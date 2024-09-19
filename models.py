from django.db import models
from django_countries.fields import CountryField


import random
import string




def generate_unique_employee_id():
    prefix = 'MEV'
    suffix = ''.join(random.choices(string.digits, k=10))
    return f'{prefix}{suffix}'


class EmployeeDetails(models.Model):
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('FT', 'Full-Time'),
        ('PT', 'Part-Time'),
        ('C', 'Contractor')
    ]
    #personal information
    first_name = models.CharField(max_length=120)
    middle_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    #contact information
    email = models.EmailField(unique=True)
    contact_number = models.CharField(unique=True, max_length=120)
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150)
    city = models.CharField(max_length=120)
    nationality = CountryField(blank_label="(select country)")
    post_or_zip = models.CharField(max_length=120)
    
    #employment infomation
    employee_id = models.CharField(unique=True, max_length=120)
    job_title = models.CharField(max_length=120)
   

    departments = models.ManyToManyField('Department', blank=True)
        
    employement_type = models.CharField(max_length=120, choices=EMPLOYMENT_TYPE_CHOICES)
    supervisor = models.CharField(null=True, max_length=120)
      
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    #additional infor
    next_of_kin = models.CharField(max_length=120)
    next_of_kin_contact = models.CharField(max_length=120)
    next_of_kin_relationship =  models.CharField(max_length=120)
    comments = models.CharField(blank=True, null=True, max_length=600)
    status = models.CharField(max_length=150)
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
  
    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = self.generate_unique_employee_id()
        super().save(*args, **kwargs)

    def generate_unique_employee_id(self):
        employee_id = generate_unique_employee_id()
        while EmployeeDetails.objects.filter(employee_id=employee_id).exists():
            employee_id = generate_unique_employee_id()
        return employee_id
    
    
    class Meta:
        verbose_name = "Employee Detail"
        verbose_name_plural = "Employee Detail"
    
   
    
    def __str__(self):
        return f"{self.first_name}  {self.id} {self.departments}"
    
       

class Department(models.Model):
    name_of_department = models.CharField(max_length=120)
    department_code = models.CharField(unique=True, max_length=120)
    department_head = models.ForeignKey('EmployeeDetails', max_length=120, null=True,  blank=True, on_delete=models.SET_NULL, related_name="department_head")
    dept_supervisors = models.ManyToManyField('EmployeeDetails', blank=True, related_name="department_super")
    description = models.CharField(max_length=500)
    created_date = models.DateField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    #Foreignkey establishes a onetomany relationship
    #department_head = models.ManyToManyField('EmployeeDetails',
    # ManyToManyField to represent the relationship between employees and 
    # departments can be useful if you want to allow multiple employees
    
    # A ManyToOne relationship in Django is represented using a ForeignKey. 
    # This is useful when you want to define a relationship where:

    # Each department can have one and only one department head.
    # One employee can be the head of multiple departments.
    
    def __str__(self):
         
        return self.name_of_department
    

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    skill_validity = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

class Training(models.Model):
    
    LOCATION = [
        ('PREMISE', 'Premise'),
        ('REMOTE', 'Remote'),
        ('HYBRID', 'Hybrid')
    ]
    
    name = models.CharField(max_length=100)
    training_provider = models.CharField(max_length=200)
    training_location = models.CharField(choices=LOCATION, max_length=200)
    description = models.TextField(blank=True, null=True)
    duration = models.DurationField()  
    start_date = models.DateField()  

    def __str__(self):
        return self.name
    
    
class EmployeeSkill(models.Model):
    
    SKILL_PROFICIENCY_LEVEL = [
        ('BEGINER', 'Beginer'),
        ('INTERMEDIATE', 'Female'),
        ('ADVANCED', 'Advanced')
    ]
    
    employee = models.ForeignKey('EmployeeDetails', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.CharField(max_length=100, choices=SKILL_PROFICIENCY_LEVEL)  #
    
    
    class Meta:
        unique_together = ('employee', 'skill')  

    def __str__(self):
        return f"{self.employee} - {self.skill} ({self.proficiency_level})"
    
    
class JobRequirement(models.Model):
    SKILL_REQUIREMENT = [
        ('BEGINER', 'Beginer'),
        ('INTERMEDIATE', 'Female'),
        ('ADVANCED', 'Advanced')
    ]
     
    job_title = models.CharField(max_length=100)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    
    # A ForeignKey establishes a one-to-many relationship, meaning that one employee can be 
    # associated with multiple departments. 
    required_level = models.CharField(max_length=100, choices=SKILL_REQUIREMENT)  # E.g., Beginner, Intermediate, Expert

    def __str__(self):
        return f"{self.job_title} requires {self.skill} ({self.required_level})"
    
    
class TrainingNeed(models.Model):
    employee = models.ForeignKey('EmployeeDetails', on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    reason = models.TextField()  # Reason why the training is needed
    expected_completion_date = models.DateField()  # When the employee should complete the training

    def __str__(self):
        return f"{self.employee} needs {self.training} (Completion by {self.expected_completion_date})"

