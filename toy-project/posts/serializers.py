from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    # def save(self, **kwargs):
    #     if 'password' in self.validated_data:
    #         # 방명록 비밀번호를 암호화하여 저장
    #         self.validated_data['password'] = make_password(self.validated_data['password'])
        
    #     return super().save(**kwargs)
    
    # 모델 인스턴스를 json으로 변환하는 메소드. 오버라이딩을 통해 password 필드가 respond 되지 않도록 한다.
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data.pop('password', None)
    #     return data