from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from django.http import HttpResponseServerError

import json

from models import *

def calcAndReturnHTTPbyJSON(a,b,c):
    """ Calculate a result and return it as json in http.
    """
    result=a+b+c
    return HttpResponse(json.dumps({"result":result}))

def getABC(request):
    """ Getting data from GET.
    """
    return (float(request.GET['a']),float(request.GET['b']),float(request.GET['c']))

def postABC(request):
    """ Getting data from POST.
    """
    return (float(request.POST['a']),float(request.POST['b']),float(request.POST['c']))

def dataFromGETwithNoCredentialReturnJSON(request):
    """ View function for GET with no credential.
    """
    try:
        (a,b,c)=getABC(request)
        return calcAndReturnHTTPbyJSON(a,b,c)
    except:
        return HttpResponseServerError(json.dumps({"error":"Something wrong","result":""}))

@csrf_exempt
def dataFromPOSTwithNoCredentialReturnJSON(request):
    """ View function for POST with no credential.
    Normally, webapi does not use cookie, so cancel csrf protection by using
    decoration.  If you want to use cookie, NEVER cancel csrf protection.
    """
    try:
        (a,b,c)=postABC(request)
        result=a+b+c
        return calcAndReturnHTTPbyJSON(a,b,c)
    except:
        return HttpResponseServerError(json.dumps({"error":"Something wrong","result":""}))

def dataFromURLwithNoCredentialReturnJSON(request,a,b,c):
    """ View function for URL with no credential.
    """
    return calcAndReturnHTTPbyJSON(int(a),int(b),int(c))



def checkCredential(credential):
    """ If credential is wrong, raise an error.
    When credential is correct, do nothing.
    """
    cred=Credential.objects.get(credential=credential)

def dataFromGETwithCredentialReturnJSON(request,credential):
    try:
        checkCredential(credential)
        (a,b,c)=getABC(request)
        return calcAndReturnHTTPbyJSON(a,b,c)
    except:
        return HttpResponseServerError(json.dumps({"error":"Something wrong","result":""}))

@csrf_exempt
def dataFromPOSTwithCredentialReturnJSON(request,credential):
    """ Django has an authentication system, however webapi will be called by
    server, so using cookie is not convenient, and we need to consider about csrf.
    This kind of "key" system is easy to use, however if you want more, please use
    oauth or something.
    """
    try:
        checkCredential(credential)
        (a,b,c)=postABC(request)
        result=a+b+c
        return calcAndReturnHTTPbyJSON(a,b,c)
    except:
        return HttpResponseServerError(json.dumps({"error":"Something wrong","result":""}))

def dataFromURLwithCredentialReturnJSON(request,credential,a,b,c):
    try:
        checkCredential(credential)
        return calcAndReturnHTTPbyJSON(int(a),int(b),int(c))
    except:
        return HttpResponseServerError(json.dumps({"error":"Something wrong","result":""}))



