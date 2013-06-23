from django.test import TestCase
from django.test.client import Client

import json

from models import *

def responseCheck(testcase,response,status_code,result):
    testcase.assertEqual(status_code,response.status_code)
    if(result!=None):
        resultin=json.loads(response.content)
        testcase.assertEqual(resultin["result"],result)

def getTestNoCredential(testcase,a,b,c,status_code,result):
    cli = Client()
    response = cli.get('/nocredential/get/?a='+str(a)+'&b='+str(b)+'&c='+str(c))
    responseCheck(testcase,response,status_code,result)

def postTestNoCredential(testcase,a,b,c,status_code,result):
    cli = Client()
    response = cli.post('/nocredential/post/',{"a":a,"b":b,"c":c})
    responseCheck(testcase,response,status_code,result)

def urlTestNoCredential(testcase,a,b,c,status_code,result):
    cli = Client()
    tempP='/nocredential/url/'+str(a)+'/'+str(b)+'/'+str(c)+'/'
    response = cli.get(tempP)
    responseCheck(testcase,response,status_code,result)

class NoCredentialTestCase(TestCase):
    urls = 'webapi_sample.urls'

    def test_dataFromGET(self):
        getTestNoCredential(self,1,2,3,200,6)
        getTestNoCredential(self,1,2.2,3,200,6.2)
        getTestNoCredential(self,"a",2,3,500,"")

    def test_dataFromPOST(self):
        postTestNoCredential(self,1,2,3,200,6)
        postTestNoCredential(self,1,2.2,3,200,6.2)
        postTestNoCredential(self,"a",2,3,500,"")

    def test_dataFromURL(self):
        urlTestNoCredential(self,1,2,3,200,6)
        urlTestNoCredential(self,1,2.2,3,404,None)
        urlTestNoCredential(self,"a",2,3,404,None)


def getTestWithCredential(testcase,credential,a,b,c,status_code,result):
    cli = Client()
    response = cli.get('/withcredential/'+str(credential)+'/get/?a='+str(a)+'&b='+str(b)+'&c='+str(c))
    responseCheck(testcase,response,status_code,result)

def postTestWithCredential(testcase,credential,a,b,c,status_code,result):
    cli = Client()
    response = cli.post('/withcredential/'+str(credential)+'/post/',{"a":a,"b":b,"c":c})
    responseCheck(testcase,response,status_code,result)

def urlTestWithCredential(testcase,credential,a,b,c,status_code,result):
    cli = Client()
    response = cli.get('/withcredential/'+str(credential)+'/url/a'+str(a)+'/b'+str(b)+'/c'+str(c)+'/')
    responseCheck(testcase,response,status_code,result)

class WithCredentialTestCase(TestCase):
    urls = 'webapi_sample.urls'

    def setUp(self):
        user=User.objects.create(username="test")
        Credential.objects.create(user=user, credential="testcred")

    def test_dataFromGET(self):
        getTestWithCredential(self,"testcred",1,2,3,200,6)
        getTestWithCredential(self,"testcred",1,2.2,3,200,6.2)
        getTestWithCredential(self,"testcred","a",2,3,500,"")
        getTestWithCredential(self,"nocred",1,2,3,500,None)

    def test_dataFromPOST(self):
        postTestWithCredential(self,"testcred",1,2,3,200,6)
        postTestWithCredential(self,"testcred",1,2.2,3,200,6.2)
        postTestWithCredential(self,"testcred","a",2,3,500,"")
        postTestWithCredential(self,"nocred",1,2,3,500,None)

    def test_dataFromURL(self):
        urlTestWithCredential(self,"testcred",1,2,3,200,6)
        urlTestWithCredential(self,"testcred",1,2.2,3,404,None)
        urlTestWithCredential(self,"testcred","a",2,3,404,None)
        urlTestWithCredential(self,"nocred",1,2,3,500,None)

