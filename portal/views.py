
from .models import PortalUser, Tasks
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView,CreateAPIView
from .serializers import RegistrationSerializers, LoginSerializer, TaskSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .authentication import PortalUserJWTAuthentication
# from django.contrib.auth import authenticate

# Create your views here.
class Registration(ListCreateAPIView):
    queryset = PortalUser.objects.all()
    serializer_class = RegistrationSerializers
    
class Login(APIView):
    def post(self, request):
        details = request.data
        seriallizer = LoginSerializer(data = details)
        if not seriallizer.is_valid():
            return Response({
                'status':False,
                'data': seriallizer.errors
            })
        role = seriallizer.validated_data['role']
        email = seriallizer.validated_data['email']
        password = seriallizer.validated_data['password']

        try:
            user = PortalUser.objects.get(email = email)
        except PortalUser.DoesNotExist:
            return Response({
                'status':False,
                'data' :"User Not Found"
            })
        if user.password != password or user.role!=role:
            return Response({
                'status':False,
                'data': "Invalid Credentials!"
            })
            
        refresh = RefreshToken.for_user(user)
        refresh['user_id'] = user.id
        refresh['role'] = user.role

        return Response({
            'status': True,
            'message': "Successfully Logged in!",
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'role': user.role
        })
        
       
    
class AdminDashboard(APIView):
    authentication_classes = [PortalUserJWTAuthentication]
    permission_classes = [IsAuthenticated]
    

    def get(self, request):
        portal_user = PortalUser.objects.get(id=request.user.id)

        if portal_user.role != 'USER_ADMIN':
            return Response({"error": "Access denied"})

        tasks = Tasks.objects.filter(assigned_by = portal_user.id)

        total_tasks = tasks.count()
        completed_tasks= tasks.filter(task_status = 'TASK_STATUS_COMPLETED').count()
        pending_tasks = total_tasks - completed_tasks

        return Response({
            'total_tasks_assigned':total_tasks,
            'pending_tasks':pending_tasks,
            'completed_tasks':completed_tasks
        })
    
class CreateTask(APIView):
    authentication_classes = [PortalUserJWTAuthentication]
    permission_classes = [IsAuthenticated]
    

    def post(self, request):

        portal_user = PortalUser.objects.get(id=request.user.id)

        if portal_user.role != 'USER_ADMIN':
            return Response({"error": "Access denied"})

        assigned_to_id = request.data.get('assigned_to')
        description = request.data.get('task_description')

        try:
            intern = PortalUser.objects.get(id = assigned_to_id, role = 'USER_INTERN')
        except PortalUser.DoesNotExist:
            return Response({'error' : "Invalid Intern Id"})
        
        task = Tasks.objects.create(
            assigned_by = portal_user,
            assigned_to = intern,
            task_description = description,
            task_status = 'TASK_STATUS_ASSIGNED'
        )

        return Response({
            "message": "Task assigned successfully",
            "Task_id": task.id
        })


    
class InternDashboard(APIView):
    authentication_classes = [PortalUserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role != 'USER_INTERN':
            return Response({"error": "Access denied"}, status=403)

        tasks = Tasks.objects.filter(assigned_to=user)

        data = [
            {
                "id": task.id,
                "description": task.task_description,
                "status": task.task_status
            }
            for task in tasks
        ]

        return Response(data)
    

class CompleteTask(APIView):
    authentication_classes = [PortalUserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, task_id):
        user = request.user

        if user.role != 'USER_INTERN':
            return Response({"error": "Access denied"}, status=403)

        try:
            task = Tasks.objects.get(id=task_id, assigned_to=user)
        except Tasks.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)

        # Optional: prevent re-completing
        if task.task_status == 'TASK_STATUS_COMPLETED':
            return Response({"message": "Task already completed"})

        task.task_status = 'TASK_STATUS_COMPLETED'
        task.save()

        return Response({"message": "Task completed successfully"})