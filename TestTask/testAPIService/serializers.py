from rest_framework import serializers
from testAPIService.models import Post

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'description',
            'published')

        ordering = ['title', 'published']