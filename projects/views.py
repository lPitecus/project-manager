from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("na verdade")


def home(request):
    return HttpResponse("Chegou aqui pq arrombado kkkkkkkkkk")