from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from apps.polls.models import Poll, PollOption, Vote
from apps.polls.serializers import PollSerializer, PollOptionSerializer, VoteSerializer

class PollViewSet(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Poll.objects.filter(trip__participants__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class PollOptionViewSet(viewsets.ModelViewSet):
    serializer_class = PollOptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PollOption.objects.filter(poll__trip__participants__user=self.request.user)

class VoteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        option_id = request.data.get("option")
        try:
            option = PollOption.objects.get(id=option_id)
        except PollOption.DoesNotExist:
            return Response({"error": "Option not found"}, status=status.HTTP_404_NOT_FOUND)

        poll = option.poll
        if poll.has_expired():
            return Response({"error": "Poll has expired"}, status=status.HTTP_400_BAD_REQUEST)

        if Vote.objects.filter(poll=poll, voted_by=request.user).exists():
            return Response({"error": "You have already voted"}, status=status.HTTP_400_BAD_REQUEST)
        
        if poll.is_multiple_choice:
            existing_votes = Vote.objects.filter(poll=poll, voted_by=request.user, option=option)
        else:
            existing_votes = Vote.objects.filter(poll=poll, voted_by=request.user)

        if existing_votes.exists():
            return Response({"error": "You have already voted"}, status=status.HTTP_400_BAD_REQUEST)


        vote = Vote.objects.create(poll=poll, option=option, voted_by=request.user)
        return Response(VoteSerializer(vote).data, status=status.HTTP_201_CREATED)
