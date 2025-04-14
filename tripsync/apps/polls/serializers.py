from rest_framework import serializers
from apps.polls.models import Poll, PollOption, Vote

class PollOptionSerializer(serializers.ModelSerializer):
    votes_count = serializers.IntegerField(source = 'votes.count', read_only=True)

    class Meta:
        model = PollOption
        fields = ['id','poll','text','votes_count']
    
class PollSerializer(serializers.ModelSerializer):
    options = PollOptionSerializer(many = True, read_only = True)
    total_votes = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ['id','trip','question','created_by','created_at','expires_at','is_active','option','total_votes']

    def get_total_votes(self,obj):
        return Vote.objects.filter(option__poll=obj).count()
    def create(self, validated_data):
        options_data = validated_data.pop('options')
        poll = Poll.objects.create(**validated_data)
        for option in options_data:
            PollOption.objects.create(poll=poll, **option)
        return poll
    

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id','user','option','voted_at']
