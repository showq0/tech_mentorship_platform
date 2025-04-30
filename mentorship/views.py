from mentorship.models import BookingSlot, Session, Mentorship
from user_auth.models import User
from mentorship.serializers import UserListSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from mentorship.permissions import IsMentor, IsMentee, IsMentorship
from rest_framework import status
from rest_framework.response import Response
from mentorship.serializers import SlotSerializer, BookSessionSerializer, AssignMentorSerializer
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError


class MentorListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(role='mentor')
    serializer_class = UserListSerializer


class MenteeListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(role='mentee')
    serializer_class = UserListSerializer


class CreateAvailableSlotsView(APIView):
    permission_classes = [IsAuthenticated, IsMentor]
    serializer_class = SlotSerializer

    def post(self, request):
        serializer = SlotSerializer(data=request.data)
        mentor_id = request.user.id
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            start_time = serializer.validated_data['start_time']
            end_time = serializer.validated_data['end_time']
            duration_minutes = serializer.validated_data['duration_minutes']
            buffer_minutes = serializer.validated_data['buffer_minutes']  # Optional

            current_date = datetime.combine(start_date, start_time)
            end_date = datetime.combine(end_date, end_time)

            # Create slots
            while current_date <= end_date:
                start_of_day = datetime.combine(current_date, start_time)
                end_of_day = datetime.combine(current_date, end_time)

                # For one day
                slot_start_time = start_of_day

                while slot_start_time + timedelta(minutes=duration_minutes) <= end_of_day:
                    BookingSlot.objects.create(
                        mentor_id=mentor_id,
                        start_time=slot_start_time,
                        duration_minutes=duration_minutes,
                        is_booked=False,
                    )
                    slot_start_time += timedelta(minutes=duration_minutes + buffer_minutes)

                current_date += timedelta(days=1)

            return Response({"message": "Available slots created successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookSessionView(APIView):
    permission_classes = [IsAuthenticated, IsMentee, IsMentorship]
    serializer_class = BookSessionSerializer

    def post(self, request, mentor_id):
        mentee_id = request.user.id
        serializer = BookSessionSerializer(data=request.data, context={'mentee_id': mentee_id})

        if serializer.is_valid():
            slot = serializer.validated_data['slot']

            if slot.mentor_id != mentor_id:
                return Response({"message": "You can only book sessions for your mentor."},
                                status=status.HTTP_400_BAD_REQUEST)

            if slot.is_booked:
                return Response({"message": "This session is not available. It has already been booked."},
                                status=status.HTTP_400_BAD_REQUEST)

            slot.is_booked = True
            slot.save()
            Session.objects.create(
                mentor_id=mentor_id,
                mentee_id=mentee_id,
                slot=slot,
            )
            return Response({"message": "Book done successfully : session at " + str(slot.start_time)},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestMentorshipView(APIView):
    # need to be done
    permission_classes = [IsAuthenticated, IsMentee]
    serializer_class = AssignMentorSerializer

    def post(self, request):
        serializer = AssignMentorSerializer(data=request.data)
        mentee_id = request.user.id
        if serializer.is_valid():
            try:
                mentor = serializer.validated_data['mentor']
                Mentorship.objects.create(
                    mentor=mentor,
                    mentee_id=mentee_id,
                )
            except ValidationError as e:
                return Response({"message": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Mentorship request sent to mentor successfully "}, status=status.HTTP_400_BAD_REQUEST)
