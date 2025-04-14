# from django.shortcuts import render
# from apps.polls.models import Poll, PollOption, Vote
# from apps.polls.serializers import PollSerializer, PollOptionSerializer, VoteSerializer
# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# # Create your views here.

# class PollList(generics.ListCreateAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = [PollSerializer]
#     permission_classes = [IsAuthenticated]
    
#     def list(self,request):
#         queryset = self.get_queryset()
#         serializer = PollSerializer(queryset, many = True)
#         return Response(serializer.data)

from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.polls.models import Poll, PollOption, Vote
from apps.polls.serializers import PollSerializer, PollOptionSerializer, VoteSerializer
from django.utils import timezone

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
            return Response({"error": "Option not found"}, status=404)

        # Prevent duplicate votes by user on same poll
        if Vote.objects.filter(user=request.user, option__poll=option.poll).exists():
            return Response({"error": "You have already voted"}, status=400)

        if option.poll.expires_at < timezone.now():
            return Response({"error": "Poll has expired"}, status=400)

        vote = Vote.objects.create(user=request.user, option=option)
        return Response(VoteSerializer(vote).data, status=201)
