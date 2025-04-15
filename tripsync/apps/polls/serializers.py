from rest_framework import serializers
from apps.polls.models import Poll, PollOption, Vote

class PollOptionSerializer(serializers.ModelSerializer):
    votes_count = serializers.IntegerField(source='votes.count', read_only=True)

    class Meta:
        model = PollOption
        fields = ['id', 'poll', 'text', 'votes_count']
        read_only_fields = ['votes_count']

class PollSerializer(serializers.ModelSerializer):
    options = PollOptionSerializer(many=True)
    total_votes = serializers.SerializerMethodField()

    class Meta: 
        model = Poll
        fields = ['id', 'trip', 'question', 'description', 'created_by', 'created_at', 'expires_at', 'is_active', 'is_multiple_choice', 'options', 'total_votes']
        read_only_fields = ['created_by', 'created_at', 'total_votes']

    def get_total_votes(self, obj):
        return obj.votes.count()

    # def create(self, validated_data):
    #     options_data = validated_data.pop('options')
    #     poll = Poll.objects.create(**validated_data)
    #     for option_data in options_data:
    #         PollOption.objects.create(poll=poll, **option_data)
    #     return poll

    def create(self, validated_data):
        options_data = validated_data.pop('options')  # Extract options data
        poll = Poll.objects.create(**validated_data)  # Create the Poll object
        for option_data in options_data:
            PollOption.objects.create(poll=poll, **option_data)  # Link options to the poll
        return poll

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'poll', 'option', 'voted_by', 'voted_at']
        read_only_fields = ['voted_by', 'voted_at']
