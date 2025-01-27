from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Osoba, Postacie, Stanowisko, Druzyna
from .permissions import CustomDjangoModelPermissions
from .serializers import OsobaSerializer, PostacieSerializer, StanowiskoSerializer, DruzynaSerializer
from django.http import Http404, HttpResponse
from django.contrib.auth import logout, login
from django.contrib import messages
from django.conf import settings
import datetime

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({"messege": "Wylogowano pomyślnie!"})

@api_view(['GET'])
def postacie_list(request):
    if request.method == 'GET':
        postacie = Postacie.objects.all()
        serializer = PostacieSerializer(postacie, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def postacie_detail(request, pk):
    if not request.user.has_perm('folder_aplikacji.change_postacie'):
        raise PermissionDenied()
    try:
        postacie = Postacie.objects.get(pk=pk)
    except Postacie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        postacie = Postacie.objects.get(pk=pk)
        serializer = PostacieSerializer(postacie)
        return Response(serializer.data)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def postacie_update(request, pk):
    try:
        postacie = Postacie.objects.get(pk=pk)
    except Postacie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = PostacieSerializer(postacie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def postacie_delete(request, pk):
    try:
        postacie = Postacie.objects.get(pk=pk)
    except Postacie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        postacie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def osoba_list(request):
    if request.method == "GET":
        if not request.user.has_perm("folder.view_postacie_other_owner"):
            osoby = Osoba.objects.filter(wlasciciel = request.user)
        else:
            osoby = Osoba.objects.all()
        serializer = OsobaSerializer(osoby, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = OsobaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(wlasciciel = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def osoba_details(request, pk):
    try:
        osoba = Osoba.objects.get(pk=pk)
    except Osoba.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = OsobaSerializer(osoba)
        return Response(serializer.data)

    elif request.method == "DELETE":
        osoba.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def osoba_search(request, substring):
    osoby = Osoba.objects.filter(imie__icontains = substring) | Osoba.objects.filter(nazwisko__icontains = substring)
    serializer = OsobaSerializer(osoby, many = True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def stanowisko_list(request):
    if request.method == 'GET':
        stanowiska = Stanowisko.objects.all()
        serializer = StanowiskoSerializer(stanowiska, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StanowiskoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'DELETE'])
def stanowisko_detail(request, pk):
    try:
        stanowisko = Stanowisko.objects.get(pk=pk)
    except Stanowisko.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StanowiskoSerializer(stanowisko)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        stanowisko.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
def welcome_view(request):
    now = datetime.datetime.now()
    html = f"""
        <html><body>
        Witaj użytkowniku! </br>
        Aktualna data i czas na serwerze: {now}.
        </body></html>"""
    return HttpResponse(html)

@login_required
@permission_required("folder_aplikacji.view_postacie")
def postacie_list_html(request):
    postacie = Postacie.objects.all()
    return render(request,
                  "folder_aplikacji/postacie/list.html",
                  {'postacie': postacie})
    
def postacie_detail_html(request, id):
    postacie = Postacie.objects.get(id=id)

    return render(request,
                  "folder_aplikacji/postacie/detail.html",
                  {'postacie': postacie})
    
def postacie_detail_html(request, id):
    try:
        postacie = Postacie.objects.get(id=id)
    except Postacie.DoesNotExist:
        raise Http404("Obiekt Postacie o podanym id nie istnieje")

    return render(request,
                  "folder_aplikacji/postacie/detail.html",
                  {'postacie': postacie})
    
def druzyna_list_html(request):
    druzyny = Druzyna.objects.all()
    return render(request,
                  "folder_aplikacji/druzyny/list.html",
                  {'druzyna': druzyny})
    
def druzyna_detail_html(request, id):
    druzyny = get_object_or_404(Druzyna, id=id)

    return render(request,
                  "folder_aplikacji/druzyny/detail.html",
                  {'druzyny': druzyny})
    
def druzyna_detail_html(request, id):
    try:
        druzyny = Druzyna.objects.get(id=id)
    except Druzyna.DoesNotExist:
        raise Http404("Obiekt Druzyna o podanym id nie istnieje")

    return render(request,
                  "folder_aplikacji/druzyny/detail.html",
                  {'druzyny': druzyny})

class StanowiskoMemberView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            stanowisko = Stanowisko.objects.get(pk=pk)
        except Stanowisko.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
        osoby = Osoba.objects.filter(stanowisko = stanowisko)
        serializer = OsobaSerializer(osoby, many = True)
        return Response(serializer.data)

class DruzynaDetail(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    def get_queryset(self):
        return Druzyna.objects.all()

    def get_object(self, pk):
        try:
            return Druzyna.objects.get(pk=pk)
        except Druzyna.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        team = self.get_object(pk)
        serializer = DruzynaSerializer(team)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        team = self.get_object(pk)
        serializer = DruzynaSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        team = self.get_object(pk)
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@csrf_exempt   
def register_user(request):
    for template_setting in settings.TEMPLATES:
        print(template_setting)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Hasła muszą się zgadzać.")
            return render(request, 'folder_aplikacji/register.html')


        if User.objects.filter(username=username).exists():
            messages.error(request, "Użytkownik o takiej nazwie już istnieje.")
            return render(request, 'folder_aplikacji/register.html')


        if User.objects.filter(email=email).exists():
            messages.error(request, "Użytkownik z takim adresem e-mail już istnieje.")
            return render(request, 'folder_aplikacji/register.html')


        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            login(request, user)

            messages.success(request, "Rejestracja przebiegła pomyślnie!")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Błąd podczas rejestracji: {e}")
            return render(request, 'folder_aplikacji/register.html')


    return render(request, 'folder_aplikacji/register.html')

def test_template(request):
    return render(request, 'folder_aplikacji/register.html')

def test_base(request):
    return render(request, 'folder_aplikaji/base.html')