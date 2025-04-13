from mentorship.models import Mentor, Mentee, BookingSlot, Session, Mentorship
from mentorship.serializers import MentorSerializer, MenteeSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from mentorship.permissions import IsMentor, IsMentee
from rest_framework import status, viewsets
from rest_framework.response import Response
from mentorship.serializers import SlotSerializer, BookSessionSerializer, AssignMentorSerializer
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated


class MentorViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer


class MenteeViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Mentee.objects.all()
    serializer_class = MenteeSerializer


class CreateAvailableSlotsView(APIView):
    permission_classes = [IsAuthenticated, IsMentor]
    serializer_class = SlotSerializer

    def post(self, request, mentor_id=None):
        serializer = SlotSerializer(data=request.data)
        is_mentor = Mentor.objects.filter(id=mentor_id).exists()
        if not is_mentor:
            return Response({"error": "Mentor can Access "},
                            status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            first_date = serializer.validated_data['first_date']
            last_date = serializer.validated_data['last_date']
            start_time = serializer.validated_data['start_time']
            end_time = serializer.validated_data['end_time']
            duration_minutes = serializer.validated_data['duration_minutes']
            buffer_minutes = serializer.validated_data['buffer_minutes']

            current_date = datetime.combine(first_date, start_time)
            last_date = datetime.combine(last_date, end_time)

            # Create slots
            while current_date <= last_date:
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
    permission_classes = [IsAuthenticated, IsMentee]
    serializer_class = BookSessionSerializer

    def post(self, request, mentee_id, mentor_id):
        serializer = BookSessionSerializer(data=request.data, context={'mentee_id': mentee_id})

        if serializer.is_valid():
            slot = serializer.validated_data['slot']
            is_mentorship = Mentorship.objects.filter(mentee_id=mentee_id, mentor_id=mentor_id).exists()

            if not is_mentorship:
                return Response({"error": "The mentor is not for mentee"},
                                status=status.HTTP_400_BAD_REQUEST)

            if slot.mentor_id != mentor_id:
                return Response({"message": "This slot not for mentor"},
                                status=status.HTTP_400_BAD_REQUEST)

            if slot.is_booked:
                return Response({"message": "This is not available_slot"},
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


class AssignMentorView(APIView):
    # need to be done
    permission_classes = [IsAuthenticated]
    serializer_class = AssignMentorSerializer

    def post(self, request, mentee_id):
        serializer = AssignMentorSerializer(data=request.data)
        if serializer.is_valid():
            mentor = serializer.validated_data['mentor']
            Mentorship.objects.create(
                mentor=mentor,
                mentee_id=mentee_id,
            )

        return Response({"message": "Assign mentor successfully "}, status=status.HTTP_400_BAD_REQUEST)
