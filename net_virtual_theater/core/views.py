from django.shortcuts import render
from rest_framework.views import APIView
from . models import *
from rest_framework.response import Response
from . serializer import *
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from django.http import HttpResponse, JsonResponse


@csrf_exempt
def join_watch_party(request):

    if request.method == 'POST':

        # Getting data from request
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        video_id = str(body['video_id'])
        username_input = str(body['username'])

        # Find a party with same jbv, status = False, and less than 3 people in the party

        get_available_parties = '''
        SELECT party_id FROM core_party WHERE video_id = \'''' + video_id + '''\' AND status = 0 AND 
        (SELECT COUNT(user_id) FROM core_user WHERE core_user.party_id = core_party.party_id) < 3 
        LIMIT 1'''

        available_party = Party.objects.raw(get_available_parties)
        party_id = ""
        user_id = str(uuid.uuid4())

        if (len(available_party) > 0):  # If there is an available party to join
            party_id = available_party[0].party_id
            user = User(user_id=user_id, username=username_input,
                        party_id=party_id)
            user.save()
        else:  # Create a new party
            party_id = str(uuid.uuid4())
            party = Party(party_id=party_id, video_id=video_id, status=False)
            party.save()

            user = User(user_id=user_id, username=username_input,
                        party_id=party.party_id)
            user.save()

        data = {
            'party_id': party_id,
            'user_id': user_id
        }
        return JsonResponse(data)
    else:
        return HttpResponse("Invalid request")


@csrf_exempt
def leave_watch_party(request):

    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        user_id = str(body['user_id'])
        party_id = str(body['party_id'])

        # If they are the only user is in the party, delete party
        # Delete user

        number_of_users_in_party = User.objects.all().filter(party_id=party_id).count()
        print(number_of_users_in_party)
        if (number_of_users_in_party == 1):
            Party.objects.filter(party_id=party_id).delete()
        User.objects.filter(user_id=user_id).delete()
        return HttpResponse("Success")


class MessageView(APIView):

    serializer_class = MessageSerializer

    def get(self, request):
        detail = [{"user_id": detail.user_id, "party_id": detail.party_id, "message": detail.message, "time_sent": detail.time_sent}
                  for detail in Message.objects.all()]
        return Response(detail)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class PartyView(APIView):

    serializer_class = PartySerializer

    def get(self, request):
        detail = [{"party_id": detail.party_id, "video_id": detail.video_id, "status": detail.status}
                  for detail in Party.objects.all()]
        return Response(detail)

    def post(self, request):
        serializer = PartySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class UserView(APIView):

    serializer_class = UserSerializer

    def get(self, request):
        detail = [{"user_id": detail.user_id, "username": detail.username, "party_id": detail.party_id}
                  for detail in User.objects.all()]
        return Response(detail)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
