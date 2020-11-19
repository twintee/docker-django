from django.http import HttpResponse
from app.models import User

def app(request):
    User.objects.create(column1='app')
    return HttpResponse('app')