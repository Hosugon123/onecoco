from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .serializers import (
    UserSerializer, UserCreateSerializer, LoginSerializer,
    ChangePasswordSerializer
)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """使用者登入"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # 更新最後登入時間
        user.save()
        
        # 生成 JWT token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': '登入成功',
            'user': UserSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """使用者登出"""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({'message': '登出成功'})
    except Exception as e:
        return Response(
            {'error': '登出失敗'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """取得當前使用者資料"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    """更新使用者資料"""
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': '資料更新成功',
            'user': serializer.data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """變更密碼"""
    serializer = ChangePasswordSerializer(
        data=request.data, 
        context={'request': request}
    )
    
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # 更新 session
        update_session_auth_hash(request, user)
        
        return Response({'message': '密碼變更成功'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListCreateView(generics.ListCreateAPIView):
    """使用者列表和建立"""
    
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """只顯示同店的使用者"""
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(store_id=self.request.user.store_id)
    
    def perform_create(self, serializer):
        """建立使用者時自動設定店面ID"""
        serializer.save(store_id=self.request.user.store_id)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """使用者詳細資料"""
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """只顯示同店的使用者"""
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(store_id=self.request.user.store_id)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_default_founders(request):
    """建立預設創始人帳號（僅超級使用者）"""
    if not request.user.is_superuser:
        return Response(
            {'error': '權限不足'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    founders_data = [
        {
            'username': 'founder1',
            'password': 'founder123',
            'first_name': '創始人',
            'last_name': '一',
            'email': 'founder1@onecoco.com',
            'role': 'founder'
        },
        {
            'username': 'founder2',
            'password': 'founder123',
            'first_name': '創始人',
            'last_name': '二',
            'email': 'founder2@onecoco.com',
            'role': 'founder'
        },
        {
            'username': 'founder3',
            'password': 'founder123',
            'first_name': '創始人',
            'last_name': '三',
            'email': 'founder3@onecoco.com',
            'role': 'founder'
        }
    ]
    
    created_users = []
    for founder_data in founders_data:
        if not User.objects.filter(username=founder_data['username']).exists():
            user = User.objects.create_user(**founder_data)
            created_users.append(user.username)
    
    if created_users:
        return Response({
            'message': f'成功建立創始人帳號: {", ".join(created_users)}'
        })
    else:
        return Response({'message': '所有創始人帳號已存在'})

