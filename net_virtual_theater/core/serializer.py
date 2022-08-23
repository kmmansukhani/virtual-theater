
from rest_framework import serializers
from . models import *
  
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['user_id', 'party_id', 'message', 'time_sent']

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ['party_id', 'jbv', 'status']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'party_id']
