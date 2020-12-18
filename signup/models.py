from django.db import models

# Create your models here.
class SignUp(models.Model):
    Userid = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Phone = models.CharField(max_length=10)
    Username = models.CharField(max_length=100)
    Password = models.CharField(max_length=32)

    def __str__(self):
        return str(self.Userid)+" "+self.Username