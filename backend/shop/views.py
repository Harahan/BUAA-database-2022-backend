from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework import status

from .models import Merchandise
from .serializers import MerchandiseSerializer
# Create your views here.


# fetch all products
# 404 if request method is not GET
# image domain is not exist
def fetchAll(request):
	if request.method == 'GET':
		merchandises = Merchandise.objects.all()
		serializer = MerchandiseSerializer(merchandises, many=True, allow_null=True)
		return JsonResponse(serializer.data, safe=False)
	return HttpResponse(status=status.HTTP_404_NOT_FOUND)
