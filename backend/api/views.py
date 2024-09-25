from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import viewsets
from django.db.models import Q
from datetime import datetime
from .serializers import *
from .models import *
#################################################################################
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
    
    def create(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        if self.request.user.is_superuser:
            query = request.query_params.get('query', '').upper()
            if query:
                profiles = Profile.objects.filter(Q(surname__icontains=query) | Q(name__icontains=query))
                users = User.objects.filter(profile__in=profiles)
                serializer = UserSerializer(users, many=True)
                return Response(serializer.data)
        return Response({"error": "Not authorized or no query provided"}, status=400)
        
    def update(self, request, *args, **kwargs):
        return Response({"error": "Update operation not allowed."}, 403)
    
    def partial_update(self, request, *args, **kwargs):
        return Response({"error": "Partial update operation not allowed."}, status=403)

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            user_id = kwargs.get('pk')
            user = User.objects.get(pk=user_id)
            user.delete()
            return Response({"success": "User deleted successfully."}, 204)
        return Response({"error": "Delete operation not allowed."}, 403)

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
#################################################################################
class AdminUserViewSet(viewsets.ModelViewSet):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
    
    def create(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            serializer = AdminUserSerializer(data=request.data)
            if serializer.is_valid():
                if User.objects.filter(username=serializer.validated_data['username']).exists():
                    return Response({"error": "A user with this username already exists."}, 400)
                
                user = User(username=serializer.validated_data['username'])
                user.set_password(serializer.validated_data['password'])
                user.save()
                
                user_serializer = AdminUserSerializer(user)
                return Response(user_serializer.data, 201)
            return Response(serializer.errors, 400)
        
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return Response({"error": "Delete operation not allowed."}, 403)
#################################################################################
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Profile.objects.all()
        return Profile.objects.filter(id=self.request.user.id)
    
    def create(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            serializer = ProfileSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    return Response(serializer.data, 201)
                except IntegrityError as e:
                    return Response(
                        {"detail": "Profile with this name and surname already exists."}, 400)
            return Response(serializer.errors, 400)
        
    @action(detail=False, methods=['get'])
    def by_week(self, request):
        if self.request.user.is_superuser:
            startOfWeek = request.query_params.get('sow')
            endOfWeek = request.query_params.get('eow')

            start_date = datetime.strptime(startOfWeek, '%d/%m/%Y')
            end_date = datetime.strptime(endOfWeek, '%d/%m/%Y')

            users = Profile.objects.filter(
                next_payment__range=(start_date, end_date)
            )

            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def until(self, request):
        if self.request.user.is_superuser:
            end_date_str = request.query_params.get('end_date')

            end_date = datetime.strptime(end_date_str, '%d/%m/%Y')

            profiles = Profile.objects.filter(next_payment__lte=end_date)

            serializer = self.get_serializer(profiles, many=True)
            return Response(serializer.data)
        
    def update(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return Response({"error": "Update operation not allowed."}, 403)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return Response({"error": "Partial update operation not allowed."}, 403)
        return super().partial_update(request, *args, **kwargs)
        
    def destroy(self, request, *args, **kwargs):
        return Response({"error": "Delete operation not allowed."}, 403)
#################################################################################       
class SessionViewSet(viewsets.ModelViewSet):
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Session.objects.all()
        return Session.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def create_session(self, request):
        sessions_data = request.data.get('sessions', [])
        created_sessions = []

        for session_data in sessions_data:
            if not request.user.is_superuser:
                session_data['user'] = request.user.id

            serializer = SessionSerializer(data=session_data)
            if serializer.is_valid():
                serializer.save()
                created_sessions.append(serializer.data)
            else:
                return Response(serializer.errors, 400)
        return Response(created_sessions, 201)

    @action(detail=False, methods=['get'])
    def by_date(self, request):
        date = request.query_params.get('date')
        date = datetime.strptime(date, '%Y-%m-%d').date()
        sessions = Session.objects.filter(date=date)
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)
        
    @action(detail=False, methods=['get'])
    def by_week(self, request):
        startOfWeek = request.query_params.get('sow')
        endOfWeek = request.query_params.get('eow')
        user = request.query_params.get('user')

        start_date = datetime.strptime(startOfWeek, '%d/%m/%Y')
        end_date = datetime.strptime(endOfWeek, '%d/%m/%Y')

        sessions = Session.objects.filter(
            user=user,
            date__range=(start_date, end_date))

        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)
            
    def update(self, request, *args, **kwargs):
        return Response({"error": "Update operation not allowed."}, status=403)

    def partial_update(self, request, *args, **kwargs):
        return Response({"error": "Partial update operation not allowed."}, status=403)
    
    def destroy(self, request, *args, **kwargs):
        session = self.get_object()
        if self.request.user.is_superuser or session.user_id == self.request.user.id:
            response = super().destroy(request, *args, **kwargs)
            return response
        return Response({"error": "You do not have permission to delete this session."}, status=403)
#################################################################################
class AdminSessionViewSet(viewsets.ModelViewSet):
    serializer_class = AdminSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Session.objects.all()
        return Session.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        if not request.user.is_superuser:
            request.data['user'] = request.user.id
        
        serializer = AdminSessionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_week(self, request):
        if self.request.user.is_superuser:
            startOfWeek = request.query_params.get('sow')
            endOfWeek = request.query_params.get('eow')
            user = request.query_params.get('user')

            start_date = datetime.strptime(startOfWeek, '%d/%m/%Y')
            end_date = datetime.strptime(endOfWeek, '%d/%m/%Y')

            sessions = Session.objects.filter(
                user=user,
                date__range=(start_date, end_date))

            serializer = self.get_serializer(sessions, many=True)
            return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_timeslot(self, request):
        if self.request.user.is_superuser:
            hour = request.query_params.get('hour')
            date = request.query_params.get('date')
            date = datetime.strptime(date, '%Y-%m-%d').date()
            sessions = Session.objects.filter(hour=hour, date=date)
            serializer = AdminSessionSerializer(sessions, many=True)
            return Response(serializer.data)
        
    def update(self, request, *args, **kwargs):
        return Response({"error": "Update operation not allowed."}, status=403)

    def partial_update(self, request, *args, **kwargs):
        return Response({"error": "Partial update operation not allowed."}, status=403)
    
    def destroy(self, request, *args, **kwargs):
        return Response({"error": "Delete operation not allowed."}, 403)
#################################################################################
class FixedSessionViewSet(viewsets.ModelViewSet):
    serializer_class = FixedSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return FixedSession.objects.all()
    
    def create(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            serializer = FixedSessionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({"error": "Update operation not allowed."}, status=408)

    @action(detail=False, methods=['get'])
    def by_user_id(self, request):
        if self.request.user.is_superuser:
            user_id = request.query_params.get('user_id')
            fixed_sessions = FixedSession.objects.filter(user_id=user_id)
            serializer = FixedSessionSerializer(fixed_sessions, many=True)
            return Response(serializer.data)
        
    def update(self, request, *args, **kwargs):
        return Response({"error": "Update operation not allowed."}, status=403)

    def partial_update(self, request, *args, **kwargs):
        return Response({"error": "Partial update operation not allowed."}, status=403)
    
    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().destroy(request, *args, **kwargs)
#################################################################################
class DisabledDateViewSet(viewsets.ModelViewSet):
    serializer_class = DisabledDateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DisabledDate.objects.all()
    
    def create(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            serializer = DisabledDateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_date(self, request):
        date = request.query_params.get('date')
        date = datetime.strptime(date, '%Y-%m-%d').date()
        ddates = DisabledDate.objects.filter(date=date)
        serializer =  DisabledDateSerializer(ddates, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_range(self, request):
        start = request.query_params.get('start')
        end = request.query_params.get('end')

        start_date = datetime.strptime(start, '%d/%m/%Y')
        end_date = datetime.strptime(end, '%d/%m/%Y')

        ddates = DisabledDate.objects.filter(date__range=(start_date, end_date))

        serializer = self.get_serializer(ddates, many=True)
        return Response(serializer.data)
        
    def update(self, request, *args, **kwargs):
        return Response({"error": "Update operation not allowed."}, status=403)

    def partial_update(self, request, *args, **kwargs):
        return Response({"error": "Partial update operation not allowed."}, status=403)
    
    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().destroy(request, *args, **kwargs)
#################################################################################
class ReschedulesViewSet(viewsets.ModelViewSet):
    serializer_class = ReschedulesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reschedules.objects.all()
    
    def create(self, request, *args, **kwargs):
        return Response({"error": "Create operation not allowed."}, status=403)

    def update(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            user = self.get_object()
            serializer = ReschedulesSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, 200)
            return Response(serializer.errors, 400)
    
    def destroy(self, request, *args, **kwargs):
        return Response({"error": "Destroy operation not allowed."}, status=403)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            reschedule = Reschedules.objects.get(user=request.user)
            serializer = self.get_serializer(reschedule)
            return Response(serializer.data)
        except Reschedules.DoesNotExist:
            return Response({"error": "Reschedules object not found for this user."}, status=404)
        

def home(request):
    return Response("Welcome to the FitMotion app!")