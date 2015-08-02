from django.test import TestCase
from django.test.client import Client

import json

from models import *
from views import *

class CredentialModelTest(TestCase):

    def setUp(self):
        self.user=User.objects.create(username="test")
        self.user.save()

    def test_1create(self):
        cred=Credential.createCred(user=self.user, id="test_api",secret="testcred")
        self.assertTrue(cred!=None)

        randSecret=Credential.generateSecret()
        cred3=Credential.createCred(user=self.user, id="test_api3",secret=randSecret)
        cred4=Credential.createCred(user=self.user, id="test_api3",secret=randSecret)
        self.assertTrue(cred3!=None)
        self.assertTrue(cred4==None)

        randID=Credential.generateID()
        cred5=Credential.createCred(user=self.user, id=randID,secret=randSecret)
        self.assertTrue(cred5!=None)

        user2=User.objects.create(username="test2")
        user2.save()
        cred6=Credential.createCred(user=user2, id="test_api",secret="testcred")
        self.assertEqual(cred6,None)

        cred7=Credential.createCred(user=user2, id="test_api4",secret="")
        self.assertEqual(cred7,None)

        cred8=Credential.createCred(user=user2, id="",secret="aaa")
        self.assertEqual(cred8,None)

        cred9=Credential.createCred(user=user2, id="test_api4",secret=None)
        self.assertEqual(cred9,None)

        cred10=Credential.createCred(user=user2, id=None,secret="aaa")
        self.assertEqual(cred10,None)

    def test_2auth(self):
        cred=Credential.createCred(user=self.user, id="test_api",secret="testcred")
        testCred=Credential.auth(id="test_api",secret="testcred")
        self.assertEqual(testCred,cred)
        self.assertEqual(testCred.user,self.user)
        self.assertTrue(testCred.hashed!="testcred")
        self.assertEqual(len(testCred.hashed),60)
        self.assertTrue(testCred.checkauth("testcred"))
        self.assertTrue(testCred.checkauth("testcred2")==False)

        cred2=Credential.createCred(user=self.user, id="test_api2",secret="testcred2")
        testCred2=Credential.auth(id="test_api2",secret="testcred2")
        self.assertEqual(testCred2,cred2)

        randSecret=Credential.generateSecret()
        cred3=Credential.createCred(user=self.user, id="test_api3",secret=randSecret)
        testCred3=Credential.auth(id="test_api3",secret=randSecret)
        self.assertEqual(testCred3,cred3)

class DummyRequest:
    def __init__(self):
        self.GET={}
        self.POST={}

class ViewTest(TestCase):

    def setUp(self):
        self.user=User.objects.create(username="test")
        self.user.save()
        self.cred=Credential.createCred(user=self.user, id="test_api",secret="testcred")

    def test_1base(self):
        response=calcAndReturnHTTPbyJSON(1,2,3)
        resultin=json.loads(response.content)
        self.assertEqual(resultin["result"],6)

        request=DummyRequest()
        request.GET={"a":1,"b":2,"c":3}
        a,b,c=getABC(request)
        self.assertEqual(a,1)
        self.assertEqual(b,2)
        self.assertEqual(c,3)

        request=DummyRequest()
        request.POST={"a":1,"b":2,"c":3}
        a2,b2,c2=postABC(request)
        self.assertEqual(a2,1)
        self.assertEqual(b2,2)
        self.assertEqual(c2,3)

    def test_2no_cred(self):
        request=DummyRequest()
        request.GET={"a":1,"b":2,"c":3}
        response=dataFromGETwithNoCredentialReturnJSON(request)
        resultin=json.loads(response.content)
        self.assertEqual(resultin["result"],6)

        request=DummyRequest()
        request.POST={"a":1,"b":2,"c":3}
        response=dataFromGETwithNoCredentialReturnJSON(request)
        resultin=json.loads(response.content)
        self.assertEqual(resultin["result"],"")

        request=DummyRequest()
        response=dataFromGETwithNoCredentialReturnJSON(request)
        resultin=json.loads(response.content)
        self.assertEqual(resultin["result"],"")

        request=DummyRequest()
        request.POST={"a":1,"b":2,"c":3}
        response=dataFromPOSTwithNoCredentialReturnJSON(request)
        resultin=json.loads(response.content)
        self.assertEqual(resultin["result"],6)

        request=DummyRequest()
        request.GET={"a":1,"b":2,"c":3}
        response=dataFromPOSTwithNoCredentialReturnJSON(request)
        resultin=json.loads(response.content)
        self.assertEqual(resultin["result"],"")

        request=DummyRequest()
        response=dataFromPOSTwithNoCredentialReturnJSON(request)
        resultin=json.loads(response.content)
        self.assertEqual(resultin["result"],"")

    def test_3cred(self):
        request=DummyRequest()
        request.GET={"a":1,"b":2,"c":3}
        response=dataFromGETwithCredentialReturnJSON(request,"test_api","testcred")
        resultin=json.loads(response.content)
        self.assertEqual(resultin["result"],6)

        request=DummyRequest()
        request.GET={"a":1,"b":2,"c":3}
        response=dataFromGETwithCredentialReturnJSON(request,"test_api","testcred2")
        resultin=json.loads(response.content)
        self.assertEqual(resultin["result"],"")

        request=DummyRequest()
        request.GET={"a":1,"b":2,"c":3}
        response=dataFromGETwithCredentialReturnJSON(request,"test_api2","testcred")
        resultin=json.loads(response.content)
        self.assertEqual(resultin["result"],"")

        request=DummyRequest()
        request.POST={"a":1,"b":2,"c":3}
        response=dataFromPOSTwithCredentialReturnJSON(request,"test_api","testcred")
        resultin=json.loads(response.content)
        self.assertEqual(resultin["result"],6)

        request=DummyRequest()
        request.POST={"a":1,"b":2,"c":3}
        response=dataFromPOSTwithCredentialReturnJSON(request,"test_api","testcred2")
        resultin=json.loads(response.content)
        self.assertEqual(resultin["result"],"")

        request=DummyRequest()
        request.POST={"a":1,"b":2,"c":3}
        response=dataFromPOSTwithCredentialReturnJSON(request,"test_api2","testcred")
        resultin=json.loads(response.content)
        self.assertEqual(resultin["result"],"")
