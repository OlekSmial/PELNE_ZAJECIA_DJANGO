from django.shortcuts import render

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Person, Team, osoba
from .serializers import PersonSerializer, osobaSerializer
from django.http import HttpResponse
import datetime
from django.http import Http404, HttpResponse
# określamy dostępne metody żądania dla tego endpointu.
@api_view(['GET'])
def person_list(request):
    """
    Lista wszystkich obiektów modelu Person.
    """
    if request.method == 'GET':
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def person_detail(request, pk):

    """
    :param request: obiekt DRF Request
    :param pk: id obiektu Person
    :return: Response (with status and/or object/s data)
    """
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    """
    Zwraca pojedynczy obiekt typu Person.
    """
    if request.method == 'GET':
        person = Person.objects.get(pk=pk)
        serializer = PersonSerializer(person)
        return Response(serializer.data)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def person_update(request, pk):

    """
    :param request: obiekt DRF Request
    :param pk: id obiektu Person
    :return: Response (with status and/or object/s data)
    """
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated]) 
def person_delete(request, pk):
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def osoba_list(request):
    if request.method == "GET":
        osoby = osoba.objects.filter(wlasciciel = request.user)
        serializer = osobaSerializer(osoby, many = True)
        return Response(serializer.data)
    if request.method == "POST" :
        serializer = osobaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(wlasciel= request.user)
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'DELATE'])
def osoba_detail(request, pk):
    try:
        osobaa = osoba.objects.get(pk=pk)
    except osoba.DoesNotExist :
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET" :
        serializer = osobaSerializer(osobaa)
        return Response(serializer.data)
    elif request.method == "DELATE":
        osobaa.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def osoba_search(request, substring):
    osobyy = osoba.objects.filter(imie__icontains = substring) | osoba.objects.filter(nazwisko__icontains = substring)
    serializer = osobaSerializer(osobyy, many = True)
    return Response(serializer.data)


# Create your views here.

def welcome_view(request):
    now = datetime.datetime.now()
    html = f"""
        <html><body>
        Witaj użytkowniku! </br>
        Aktualna data i czas na serwerze: {now}.
        </body></html>"""
    return HttpResponse(html)

def person_list_html(request):
    # pobieramy wszystkie obiekty Person z bazy poprzez QuerySet
    persons = Person.objects.all()
    return render(request,
                  "folder_aplikacji/person/list.html",
                  {'persons': persons})

def person_detail_html(request, id):
    # pobieramy konkretny obiekt Person
    try:
        person = Person.objects.get(id=id)
    except Person.DoesNotExist:
        raise Http404("Obiekt Person o podanym id nie istnieje")

    return render(request,
                  "folder_aplikacji/person/detail.html",
                  {'person': person})
