from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200,unique=True)
    password = models.CharField(max_length=256)

    def __str__(self) :
        return self.name
    
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    taskTitle = models.CharField(max_length=200)
    taskDesc = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"USER-{self.user} , TASK-{self.taskTitle} , ID-{self.id}"