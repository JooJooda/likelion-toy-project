from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PostSerializer
from django.http import Http404
from rest_framework import status
from posts.models import *
from django.shortcuts import get_object_or_404 
from django.contrib.auth.hashers import check_password


class PostList(APIView):
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        post = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)
    
class PostDetail(APIView):
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, id):
        post = get_object_or_404(Post, id=id)

        if 'password' not in request.data:
            return Response({"error":"비밀번호를 입력하세요"}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data['password'] != post.password:
            return Response({"error":"비밀번호가 일치하지 않습니다. 수정 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST )  
        
        # partial = True는 부분 업데이트 허용
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        post = get_object_or_404(Post, id=id)
        if 'password' not in request.data:
            return Response({"error":"비밀번호를 입력하세요"}, status=status.HTTP_400_BAD_REQUEST)

        # 암호화된 비밀번호와 사용자가 입력한 비밀번호를 비교
        if request.data['password'] != post.password:
            return Response({"error":"비밀번호가 일치하지 않습니다"}, status=status.HTTP_400_BAD_REQUEST )  
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
