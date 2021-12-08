from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from django.db import connection
import json
from rest_framework.authtoken.views import APIView
from django.contrib.auth.models import User


class order_inquiry(APIView):
    def get(self,request,*args, **kwargs):
        if request.method == 'GET':

            print("receive GET request at /order_inquiry")
            user_id = request.GET.get('user_id')
            if User.objects.filter(username=user_id).exists():

                resp = {
                    'id': 0,
                    'msg': 'Success',
                    'payload': {
            "order_id": "订单号",
            "mer_name": "店铺名",
            "goods_name": "商品名",
            "image": "商品图片src",
            "num": "购买数量",
            "amount":"金额"
        }
                }
            else:
                inquiry_sql = 'select'
