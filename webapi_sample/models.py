from django.db import models
from django.contrib.auth.models import User
import random
import bcrypt

class Credential(models.Model):
    user = models.ForeignKey(User, related_name='webapi_credential')
    idName=models.CharField(max_length=60)
    hashed=models.CharField(max_length=60)

    @classmethod
    def createCred(cls,user, id,secret):
        if(secret=="" or secret==None or id=="" or id==None):
            return None
        target = Credential.objects.filter(idName=id)
        if(target.count()>0):
            return None
        hashed = bcrypt.hashpw(secret, bcrypt.gensalt())
        target = Credential(user=user,idName=id,hashed=hashed)
        target.save()
        return target

    @classmethod
    def auth(cls,id,secret):
        target = Credential.objects.filter(idName=id)
        if(target.count()!=1):
            return None
        if(target[0].checkauth(secret)):
            return target[0]
        return None

    @classmethod
    def generateID(cls,num=30):
        tempStr=""
        for i in range(1, num):
            tempStr+=random.choice("1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-+")
        return tempStr

    @classmethod
    def generateSecret(cls,num=128):
        tempStr=""
        for i in range(1, num):
            tempStr+=random.choice("1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_@+.-[]/^|?*")
        return tempStr

    def checkauth(self,secret):
        if bcrypt.hashpw(secret, self.hashed.encode('utf-8')) == self.hashed:
            return True
        else:
            return False
