from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .serializers import LogSerializer
from .services import *  # Ensure these functions are properly defined

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            response = super().post(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                tokens = response.data
                response.set_cookie(
                    key='access_token',
                    value=tokens['access'],
                    httponly=True,
                    secure=True,  # Set to True in production
                    samesite='Lax'
                )
                response.set_cookie(
                    key='refresh_token',
                    value=tokens['refresh'],
                    httponly=True,
                    secure=True,  # Set to True in production
                    samesite='Lax'
                )
            return response
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        
class LogViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Optionally, admins can see all logs
        try:
            logs = get_logs()
            serializer = LogSerializer(logs, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        # Logs added by drivers
        serializer = LogSerializer(data=request.data)
        if serializer.is_valid():
            try:
                add_log(serializer.validated_data)
                return Response({"status": "Log created"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            log = get_log_by_id(pk)
            if log:
                serializer = LogSerializer(log)
                return Response(serializer.data)
            return Response({"error": "Log not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            log = get_log_by_id(pk)
            if log:
                serializer = LogSerializer(log, data=request.data, partial=True)
                if serializer.is_valid():
                    try:
                        update_log(pk, serializer.validated_data)
                        return Response({"status": "Log updated"})
                    except Exception as e:
                        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "Log not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            log = get_log_by_id(pk)
            if log:
                try:
                    delete_log(pk)
                    return Response({"status": "Log deleted"})
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({"error": "Log not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='by-driver/(?P<driver_id>[^/.]+)')
    def by_driver(self, request, driver_id=None):
        try:
            logs = get_logs_by_driver(driver_id)
            serializer = LogSerializer(logs, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='by-car/(?P<car_id>[^/.]+)')
    def by_car(self, request, car_id=None):
        try:
            logs = get_logs_by_car(car_id)
            serializer = LogSerializer(logs, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='by-date/(?P<date>[^/.]+)')
    def by_date(self, request, date=None):
        try:
            logs = get_logs_by_date(date)
            serializer = LogSerializer(logs, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='approve')
    def approve_log(self, request, pk=None):
        try:
            log = get_log_by_id(pk)
            if log:
                update_log(pk, {'status': 'approved'})  # Example status field
                return Response({"status": "Log approved"})
            return Response({"error": "Log not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='disapprove')
    def disapprove_log(self, request, pk=None):
        try:
            log = get_log_by_id(pk)
            if log:
                update_log(pk, {'status': 'disapproved'})  # Example status field
                return Response({"status": "Log disapproved"})
            return Response({"error": "Log not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
