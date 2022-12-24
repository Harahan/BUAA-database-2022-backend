from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Chat, Record
from .serializers import ChatSerializer, RecordSerializer
# Create your views here.
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from fuzzywuzzy import fuzz
from user.models import User


def get_chats(request):
	if request.method == 'GET':
		if not request.user.is_authenticated:
			return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
		if not request.GET.get('name'):
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
		else:
			name = request.GET.get('name')
			rt = []
			if Chat.objects.filter(name=name, type="group").exists():
				chats = Chat.objects.filter(name=name, type="group")
				serializer = ChatSerializer(chats, many=True)
				for data in serializer.data:
					rt.append(data)
			if Chat.objects.filter(member__username=name, type="private").exists():
				chats = Chat.objects.filter(member__username=name, type="private")
				serializer = ChatSerializer(chats, many=True)
				for data in serializer.data:
					rt.append(data)
			if rt:
				# rt.sort(key=lambda x: x['latest']['originalTime'], reverse=True)
				return JsonResponse(rt, safe=False)
			else:
				for chat in Chat.objects.all():
					if chat.type == "group" and fuzz.ratio(chat.name, name) > 70:
						rt.append(ChatSerializer(chat).data)
					if chat.type == "private":
						for member in chat.member.all():
							if fuzz.ratio(member.username, name) > 70:
								rt.append(ChatSerializer(chat).data)
								break
				return JsonResponse(rt, safe=False)

			
''''
def find_user(request):
	if request.method == 'GET':
		chat_id = request.GET.get('id')
		username = request.GET.get('username')
		if Record.objects.filter(chat=chat_id, user__username=username).exists():
			# latest = Record.objects.filter(chat=chat_id, user__username=username).order_by('-originalTime').first()
			serializer = RecordSerializer(latest)
			return JsonResponse(serializer.data, safe=False)
		else:
			return JsonResponse({}, safe=False)
'''


@csrf_exempt
def create_chat(request):
	if request.method == 'POST':
		if not request.user.is_authenticated:
			return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
		if not request.POST.get('name'):
			# if the private chat exists, return it
			for chat in Chat.objects.all():
				if chat.type == "private" and chat.member.count() == 2:
					x = chat.member.all()[0].username
					y = chat.member.all()[1].username
					if request.POST.get('username') == x + "," + y or request.POST.get('username') == y + "," + x:
						return JsonResponse(ChatSerializer(chat).data, safe=False)
			chat = Chat.objects.create(name=request.POST.get('username').replace(",", "_"), type="private", owner=request.user)
		else:
			chat = Chat.objects.create(name=request.POST.get('name'), type="group", owner=request.user)
		for username in request.POST.get('username').split(','):
			user = User.objects.get(username=username)
			chat.member.add(user)
		chat.save()
		return JsonResponse(ChatSerializer(chat).data, safe=False)
		
		
def get_records(request):
	if request.method == 'GET':
		chat_id = request.GET.get('id')
		if Record.objects.filter(chat=chat_id).exists():
			records = Record.objects.filter(chat=chat_id)
			serializer = RecordSerializer(records, many=True)
			rt = []
			for s in serializer.data:
				if s['username'] == request.user.username:
					s['sender'] = 0
				else:
					s['sender'] = 1
				rt.append(s)
			if rt:
				rt = sorted(rt, key=lambda x: x['originalTime'], reverse=True)
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
		records = Record.objects.filter(chat=chat_id)
		serializer = RecordSerializer(records, many=True)
		rt = []
		for s in serializer.data:
			if s['username'] == request.user.username:
				s['sender'] = 0
			else:
				s['sender'] = 1
			rt.append(s)
		if rt:
			rt = sorted(rt, key=lambda x: x['originalTime'], reverse=True)
		return JsonResponse(rt, safe=False)
		
	return JsonResponse([], safe=False)


@csrf_exempt
def add_member(request):
	if request.method == 'POST':
		chat_id = request.POST.get('id')
		chat = Chat.objects.get(id=chat_id)
		for username in request.POST.get('username').split(','):
			if User.objects.filter(username=username).exists() and not chat.member.filter(username=username).exists():
				user = User.objects.get(username=username)
				chat.member.add(user)
		chat.save()
		return JsonResponse(ChatSerializer(chat).data, safe=False)