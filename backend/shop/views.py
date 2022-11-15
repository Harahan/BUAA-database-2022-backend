from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
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
		if merchandises:
			serializer = MerchandiseSerializer(merchandises, many=True, allow_null=True)
			return JsonResponse(serializer.data, safe=False)
		else:
			JsonResponse([], safe=False)
	return HttpResponse(status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def fetch_user_merchandises(request):
	if request.method == 'POST':
		# frontend should check if user is authenticated
		user = request.user
		merchandises = Merchandise.objects.filter(username=user)
		if not merchandises:
			return JsonResponse([], safe=False)
		serializer = MerchandiseSerializer(merchandises, many=True)
		op = request.POST.get('op')
		serializer_data = sorted(serializer.data, key=lambda x: x['originalTime'], reverse=True if int(op) == 0 else False)
		return JsonResponse(serializer_data, safe=False)