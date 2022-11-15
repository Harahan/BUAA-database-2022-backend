from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Chat, Record
from .serializers import ChatSerializer, RecordSerializer
# Create your views here.
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt


def get_chats(request):
	if request.method == 'GET':
		if not request.user.is_authenticated:
			return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
		
		user = request.user
		if user.chat_member.exists():
			# print(user.chat_member.all())
			# print(user)
			chats = user.chat_member.all()
			serializer = ChatSerializer(chats, many=True, allow_null=True)
			rt = []
			for data in serializer.data:
				if data['latest']:
					rt.append(data)
			rt.sort(key=lambda x: x['latest']['originalTime'], reverse=True)
			return JsonResponse(rt, safe=False)
		else:
			return JsonResponse([], safe=False)
		
		
def find_user(request):
	if request.method == 'GET':
		chat_id = request.GET.get('id')
		username = request.GET.get('username')
		if Record.objects.filter(chat=chat_id, user__username=username).exists():
			latest = Record.objects.filter(chat=chat_id, user__username=username).order_by('-originalTime').first()
			serializer = RecordSerializer(latest)
			return JsonResponse(serializer.data, safe=False)
		else:
			return JsonResponse({}, safe=False)
		
		
def get_records(request):
	if request.method == 'GET':
		chat_id = request.GET.get('id')
		if Record.objects.filter(chat=chat_id).exists():
			records = Record.objects.filter(chat=chat_id).order_by('-originalTime')
			serializer = RecordSerializer(records, many=True)
			rt = []
			for s in serializer.data:
				if s['username'] == request.user.username:
					s['sender'] = 0
				else:
					s['sender'] = 1
				rt.append(s)
			return JsonResponse(rt, safe=False)
		return JsonResponse([], safe=False)
	
	
@csrf_exempt
def send_record(request):
	if request.method == 'POST':
		chat_id = request.POST.get('id')
		content = request.POST.get('content')
		chat = Chat.objects.get(id=chat_id)
		record = Record.objects.create(chat=chat, user=request.user, content=content)
		record.save()
		# serializer = RecordSerializer(record)
		records = Record.objects.filter(chat=chat_id).order_by('-originalTime')
		serializer = RecordSerializer(records, many=True)
		rt = []
		for s in serializer.data:
			if s['username'] == request.user.username:
				s['sender'] = 0
			else:
				s['sender'] = 1
			rt.append(s)
		return JsonResponse(rt, safe=False)
		
	return JsonResponse([], safe=False)
