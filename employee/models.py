from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser




# Create your models here.


class myuser_model(AbstractUser):

    # status=models.BooleanField(default=False)
    status=models.CharField(max_length=30,
    choices=(
            ('APPROVE','approve'),
            ('REJECT','reject')
            )
        )


class empleave_model(models.Model):
    
    name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    from1=models.DateField()
    to1=models.DateField()
    day=models.CharField(max_length=30,
        choices=(
            ('HALF DAY','Half day') ,
            ('FULL DAY','Full day'),
            )
            )

    reason=models.TextField()  

    def __str__(self):
        return self.name




