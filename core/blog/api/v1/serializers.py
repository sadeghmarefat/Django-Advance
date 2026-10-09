
from rest_framework import serializers

from accounts.models import Profile
from ...models import Post, Category

# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.CharField(source='get_snippet', read_only=True)
    relative_url = serializers.CharField(source='get_absolute_api_url', read_only=True)
    abs_url = serializers.SerializerMethodField()
    author = serializers.CharField(source='author.first_name', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'category', 'content','status', 'snippet', 'abs_url', 'relative_url', 'created_at', 'published_at']
        read_only_fields = ['author']

    def get_abs_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_api_url())

    def to_representation(self, instance):
        request = self.context.get('request')
        data = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('pk'):
            data.pop('relative_url')
            data.pop('abs_url')
            data.pop('snippet')
        else:
            data.pop('content')
        data['Category'] = CategorySerializer(instance.category).data
        return data

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)