from rest_framework import serializers

from webapp.models import Commentary, Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(max_length=25)
    title = serializers.CharField(max_length=50)
    text = serializers.CharField(style={'base_template'})

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'text']


class RecursiveField(serializers.ModelSerializer):
    def to_native(self, value):
        return CommentListSerializer(value, context={"parent": self.parent.object, "parent_serializer": self.parent})


class CommentListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    post = serializers.ReadOnlyField(source='post.author')
    author = serializers.CharField(max_length=25)
    content = serializers.CharField(style={'base_template'})
    date_add = serializers.DateTimeField()
    approved_comment = serializers.BooleanField(default=False)
    children = RecursiveField(many=True, required=False)

    class Meta:
        model = Commentary
        fields = ['id', 'post', 'author', 'content', 'date_add', 'approved_comment', 'children']


class ChildrenBoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        exclude = ['lft']


class CommentarySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    post = serializers.ReadOnlyField(source='p ost.id')
    author = serializers.CharField(max_length=25)
    content = serializers.CharField(style={'base_template'})
    date_add = serializers.DateTimeField()
    approved_comment = serializers.BooleanField(default=False)
    children = ChildrenBoneSerializer(many=True)

    class Meta:
        model = Commentary
        exclude = ['lft']

    def get_leaf_nodes(self, obj):
        return CommentarySerializer(obj.get_children(), many=True).data


class CommentaryTreeSerializer(serializers.ModelSerializer):
    children = serializers.ListField(child=RecursiveField())

    class Meta:
        model = Commentary
        fields = ('id', 'name', 'plural_name', 'children',)
