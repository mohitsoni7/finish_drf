from django.http import Http404
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import mixins
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics


from .models import Snippet
from .serializers import SnippetModelSerializer


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

class SnippetDetail4(generics.RetrieveUpdateDestroyAPIView):
	lookup_field = 'id'
	queryset = Snippet.objects.all()
	serializer_class = SnippetModelSerializer
