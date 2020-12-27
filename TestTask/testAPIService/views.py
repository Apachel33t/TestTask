from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from testAPIService.models import Post
from testAPIService.serializers import PostSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class PostView(APIView):
    permission_classes = (IsAuthenticated,)

    @api_view(['GET', 'POST', 'DELETE'])
    def post_list(request):
        if request.method == 'GET':
            paginator = PageNumberPagination()
            paginator.page_size = 10
            post = Post.objects.all()
            title = request.GET.get('title', None)
            if title is not None:
                post = post.filter(title__icontains=title)

            result_page = paginator.paginate_queryset(post, request)
            post_serializer = PostSerializer(result_page, many=True)
            return paginator.get_paginated_response(post_serializer.data)
        elif request.method == 'POST':
            post_data = JSONParser().parse(request)
            post_serializer = PostSerializer(data=post_data)
            if post_serializer.is_valid():
                post_serializer.save()
                return JsonResponse(post_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            count = Post.objects.all().delete()
            return JsonResponse({'message': '{} Posts deleted'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

    @api_view(['GET', 'PUT', 'DELETE'])
    def post_detail(request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return JsonResponse({'message': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            post_serializer = PostSerializer(post)
            return JsonResponse(post_serializer.data)
        elif request.method == 'PUT':
            post_data = JSONParser().parse(request)
            post_serializer = PostSerializer(post, data=post_data)
            if post_serializer.is_valid():
                post_serializer.save()
                return JsonResponse(post_serializer.data)
            return JsonResponse(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            post.delete()
            return JsonResponse({'message': 'Post was deleted'}, status=status.HTTP_204_NO_CONTENT)

    @api_view(['GET'])
    def post_list_published(request):
        post = Post.objects.filter(post_list_published=True)

        if request.method == 'GET':
            post_serializer = PostSerializer(post, many=True)
            return JsonResponse(post_serializer.data, safe=False)



