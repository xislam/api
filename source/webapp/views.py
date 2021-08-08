from django.http import Http404
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from webapp.models import Commentary, Post
from webapp.serializers import CommentarySerializer, CommentaryTreeSerializer, PostSerializer


class PostList(APIView):
    """
    List all snippets, or create a new post.
        """

    def get(self, request, format=None):
        snippets = Post.objects.all()
        serializer = PostSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    """
    Retrieve, update or delete a post instance.
    """

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = PostSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = PostSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """This endpoint list all of the available category from the database"""
    queryset = Commentary.objects.all()
    serializer_class = CommentarySerializer
    pagination_class = None

    def get(self, *args, **kwargs):
        categories = Commentary.objects.filter(level=0).all()
        serializer = CommentaryTreeSerializer(categories, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

