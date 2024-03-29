from django.contrib.auth.models import User
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import renderers
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets

from .models import Snippet
from .permissions import IsOwnerOrReadOnly
from .serializers import SnippetModelSerializer, UserModelSerializer, SnippetHyperlinkedModelSerializer, UserHyperlinkedModelSerializer, SnippetHighlightSerializer


@csrf_exempt
def snippet_list(request):
    """
    Returns:
        1. JSON of all Snippet List for GET request
        2. Create a new Snippet for POST request for validated_data
    """
    if request.method =='GET':
        serializer = SnippetModelSerializer(Snippet.objects.all(), many=True)
        return(JsonResponse(serializer.data, safe=False))

    elif request.method == 'POST':
        data = JSONParser.parse(request)
        serializer = SnippetModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return(JsonResponse(serializer.data, status=201))
        return(JsonResponse(serializer.errors, status=400))


@csrf_exempt
def snippet_detail(request, id):
    """
    1. GET: Returns the detail of a particular Snippet
    2. PUT: Updates the detail of a particular Snippet
    3. DELETE: Deletes a particular Snippet
    """
    try:
        snippet = Snippet.objects.get(id=id)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetModelSerializer(snippet)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser.parse(request)
        serializer = SnippetModelSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)

# ===========================================================================================================

@api_view(['GET', 'POST'])
def snippet_list2(request, format=None):
    """
    Returns:
        1. JSON of all Snippet List for GET request
        2. Create a new Snippet for POST request for validated_data
    """
    if request.method =='GET':
        serializer = SnippetModelSerializer(Snippet.objects.all(), many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail2(request, id, format=None):
    """
    1. GET: Returns the detail of a particular Snippet
    2. PUT: Updates the detail of a particular Snippet
    3. DELETE: Deletes a particular Snippet
    """
    try:
        snippet = Snippet.objects.get(id=id)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetModelSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetModelSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ====================================================================================================================


class SnippetList(APIView):
    """
    List of all Snippets or Create a new Snippet
    """
    def get(self, request, format=None):
        serializer = SnippetModelSerializer(Snippet.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetModelSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    """
    Detail, Update and Delete
    """
    def get_object(self, id):
        try:
            snippet = Snippet.objects.get(id=id)
            return snippet
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        """
        Returns Snippet Details
        """
        snippet = self.get_object(id)
        serializer = SnippetModelSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        snippet = self.get_object(id)
        serializer = SnippetModelSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        snippet = self.get_object(id)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# =================================================================================================

class SnippetList2(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    1. List for GET request
    2. Create Snippets for POST requests
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class SnippetDetail2(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    1. GET request: Returns details of a Snippet
    1. PUT request: Update a Snippet
    1. DELETE request: Deletes a Snippet
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.destroy(self, request, *args, **kwargs)

# ====================================================================================================

class SnippetList3(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer

class SnippetDetail3(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer

# ====================================================================================================

class SnippetList4(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail4(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

# =====================================================================================================
# Creatting an endpoint for the root of our API
# single entry point for our API

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
            'users': reverse('user-list', request=request, format=format),
            'snippets': reverse('snippet-list', request=request, format=format),
        })


class SnippetHighlight(generics.ListAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetHighlightSerializer
    renderer_classes = [renderers.StaticHTMLRenderer]  

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

# ====================================================================================================


class SnippetList5(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetHyperlinkedModelSerializer


class SnippetDetail5(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetHyperlinkedModelSerializer


class UserList2(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserHyperlinkedModelSerializer

class UserDetail2(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserHyperlinkedModelSerializer


# =====================================================================================================

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A Viewset for viewing Users and Retrieving Users.
    """
    queryset = User.objects.all()
    serializer_class = UserHyperlinkedModelSerializer

    def list(self, serializer):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True, context={'request': self.request})
        print(serializer.data)
        return Response(serializer.data)



class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetHyperlinkedModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

