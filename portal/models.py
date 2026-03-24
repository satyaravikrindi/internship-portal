from django.db import models

# Create your models here.

class PortalUser(models.Model):
    @property
    def is_authenticated(self):
        return True
    
    ROLE_CHOICES = [
        ('USER_ADMIN','Admin'),
        ('USER_INTERN','Intern')
    ]
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique= True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES)

class Tasks(models.Model):
    TASK_STATUS_CHOICES =[
        ('TASK_STATUS_PENDING','Pending'),
        ('TASK_STATUS_ASSIGNED','Assigned'),
        ('TASK_STATUS_COMPLETED','Completed')
    ]
    assigned_by = models.ForeignKey(PortalUser, on_delete=models.PROTECT, related_name='task_assigned_by')
    assigned_to = models.ForeignKey(PortalUser, on_delete=models.PROTECT, related_name='task_assigned_to')
    task_description = models.CharField(max_length=255)
    task_status = models.CharField(max_length=255, choices=TASK_STATUS_CHOICES, default='TASK_STATUS_PENDING')