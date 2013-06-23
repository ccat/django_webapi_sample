==============================================
django_webapi_sample: Sample application of webapi on django.
==============================================

Description
============
Sample Django Application of WebAPI provider, not a client.
This application will get values a,b,c by GET, POST or URL and return a+b+c by JSON.

For example, following URL is the URL of GET pattern.
https://whiteblack-cat.info/ja/webapi_sample/nocredential/get/?a=1&b=2&c=3
This returns "{"result": 6.0}".

Requirements
============
* Django


解説
============
WebAPIを提供するDjango Applicationのサンプルです。
GET、POSTかURLからa,b,cの値を取得して、足し算した結果をJSONで返します。

たとえば、下記のURLにアクセスすると「{"result": 6.0}」が戻されます。

https://whiteblack-cat.info/ja/webapi_sample/nocredential/get/?a=1&b=2&c=3

もう少し詳細な解説は下記に記載してあります。
https://whiteblack-cat.info/ja/django-tips/django-webapi/

依存関係
============
* Django

