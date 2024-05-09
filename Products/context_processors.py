# yourapp/context_processors.py
from django.contrib.auth.models import Group

def exporter_status(request):
    exporter = None
    if request.user.is_authenticated:
        exporter = request.user.groups.filter(name='Exporter')
    return {'Exporter': exporter}
