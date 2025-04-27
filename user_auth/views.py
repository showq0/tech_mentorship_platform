from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from user_auth.serializers import RegisterSerializer, ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response({"message": "User created successfully.", "tokens": tokens}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self,request):
        profile_info = request.user.profile_info
        return Response({"profile_info": profile_info}, status=status.HTTP_201_CREATED)

    def post(self, request):
        is_mentor = (request.user.role == "mentor")
        serializer = ProfileSerializer(data=request.data, context= {'is_mentor': is_mentor})
        if serializer.is_valid():
            request.user.profile_info = serializer.validated_data['profile_info']
            request.user.save()

            return Response({"message": "Profile info updated successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
