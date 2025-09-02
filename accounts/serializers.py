from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """使用者詳細資料序列化器"""
    
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """使用者序列化器"""
    
    profile = UserProfileSerializer(read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'role_display', 'store_id', 'phone', 'is_active',
            'date_joined', 'last_login', 'profile'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']


class UserCreateSerializer(serializers.ModelSerializer):
    """使用者建立序列化器"""
    
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'role', 'phone'
        ]
    
    def validate(self, attrs):
        """驗證密碼確認"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("密碼確認不匹配")
        return attrs
    
    def create(self, validated_data):
        """建立使用者"""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """登入序列化器"""
    
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        """驗證登入憑證"""
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('使用者名稱或密碼錯誤')
            if not user.is_active:
                raise serializers.ValidationError('使用者帳號已被停用')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('必須提供使用者名稱和密碼')
        
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """變更密碼序列化器"""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        """驗證密碼"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("新密碼確認不匹配")
        return attrs
    
    def validate_old_password(self, value):
        """驗證舊密碼"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("舊密碼錯誤")
        return value

