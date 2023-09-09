from django.db import models
from django.contrib.auth.models import User  #this model is aldready predefined by django itself and we are
                                            #importing it.
# Create your models here.
class Topic(models.Model):
    topic=models.CharField(max_length=1000)

    def __str__(self):
        return (self.topic)

class Room (models.Model):
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    updated_models=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    #To keep these room details in an descending order, creat a Meta class
    class Meta:
        ordering=['-updated_models','created']
        #The above 2 lines is the method to sort the data in descending order
        # "-"indicates that it is sorting in descending order
        #if we remove "-" it sorts normally

    def __str__(self):
        return (self.name)

class Message(models.Model):
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
#The following error will occur when i write the above line of code
    #It is impossible to add the field 'created' with 'auto_now_add=True' to message without providing a default.
    #This is because the database needs seomething to popurlate existing rows
    #Reason: We are trying to add time of creation timestamps to the aldready created data so that's why we have
    #to provide default timezont to it as second parameter.

    def __str__(self):
        return self.body[:50]

