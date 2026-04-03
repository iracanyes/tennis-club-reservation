import json
from django.http import HttpResponse

def welcome(request):
  return HttpResponse(json.dumps({'code': 200, 'message': 'Welcome!'}), content_type="application/json")