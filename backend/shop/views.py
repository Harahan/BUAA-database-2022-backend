from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from user.models import User
from .models import Merchandise, COLOR
from .serializers import MerchandiseSerializer
# Create your views here.


# fetch all products
# 404 if request method is not GET
# image domain is not exist
def fetch_all(request):
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
		if not User.objects.filter(username=request.POST.get('username')).exists():
			return JsonResponse([], safe=False)
		user = User.objects.get(username=request.POST.get('username'))
		merchandises = Merchandise.objects.filter(username=user)
		if not merchandises:
			return JsonResponse([], safe=False)
		serializer_data = MerchandiseSerializer(merchandises, many=True).data
		# op = request.POST.get('op')
		# serializer_data = sorted(serializer.data, key=lambda x: x['originalTime'], reverse=True if int(op) == 0 else False)
		if request.POST.get('sale') == 'true':
			serializer_data = [x for x in serializer_data if x['status'] == 1]
		elif request.POST.get('new') == 'true':
			serializer_data = [x for x in serializer_data if x['status'] == 2]
		if not serializer_data:
			return JsonResponse([], safe=False)
		if request.POST.get('category') != "":
			serializer_data = [x for x in serializer_data if x['category'] == request.POST.get('category')]
		if not serializer_data:
			return JsonResponse([], safe=False)
		if request.POST.get('color') != "":
			y = 0
			for x in request.POST.get('color').split(','):
				# print(x)
				y += COLOR[x]
			serializer_data = [x for x in serializer_data if (x['color_num'] & y) == y]
		if not serializer_data:
			return JsonResponse([], safe=False)
		if int(request.POST.get('priceSale')) == 0:
			serializer_data = [x for x in serializer_data if x['priceSale'] <= 25]
		elif int(request.POST.get('priceSale')) == 1:
			serializer_data = [x for x in serializer_data if 25 < x['priceSale'] <= 75]
		else:
			serializer_data = [x for x in serializer_data if 75 < x['priceSale']]
		if not serializer_data:
			return JsonResponse([], safe=False)
		serializer_data = [x for x in serializer_data if x['rank'] >= int(request.POST.get('rank'))]
		if not serializer_data:
			return JsonResponse([], safe=False)
		if int(request.POST.get('op')) == 0:
			serializer_data = sorted(serializer_data, key=lambda x: x['originalTime'], reverse=True)
		elif int(request.POST.get('op')) == 1:
			serializer_data = sorted(serializer_data, key=lambda x: x['rank'], reverse=True)
		elif int(request.POST.get('op')) == 2:
			serializer_data = sorted(serializer_data, key=lambda x: x['priceSale'], reverse=True)
		else:
			serializer_data = sorted(serializer_data, key=lambda x: x['priceSale'])
		return JsonResponse(serializer_data, safe=False)
	
	
@csrf_exempt
def post_merchandise(request):
	if request.method == 'POST':
		user = request.user
		if not user.is_authenticated:
			return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
		color = request.POST.get('color').split(',')
		c = 0
		for x in list(color):
			c += COLOR[x]
		merchandise = Merchandise.objects.create(
			username=user,
			name=request.POST.get('name'),
			category=request.POST.get('category'),
			deliveryTime=request.POST.get('deliveryTime'),
			deliveryLocation=request.POST.get('deliveryLocation'),
			color=c,
			description=request.POST.get('description'),
			image=request.FILES.get('image'),
			price=float(request.POST.get('price')),
			priceSale=float(request.POST.get('priceSale')),
		)
		merchandise.save()
		return HttpResponse(status=status.HTTP_200_OK)
	return HttpResponse(status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def get_merchandise(request):
	if request.method == 'POST':
		if not Merchandise.objects.filter(id=request.POST.get('id')).exists():
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		merchandise = Merchandise.objects.get(id=request.POST.get('id'))
		serializer = MerchandiseSerializer(merchandise)
		return JsonResponse(serializer.data, safe=False)
	return HttpResponse(status=status.HTTP_404_NOT_FOUND)
