from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

from .models import Museo

# Create your views here.
@login_required()
@permission_required('subvenciones.can_add_subvencion', raise_exception=True)
def index_museo(request):
    museos = Museo.objects.all().select_related(
        'tipus', 'classe'
        )

    return render(request,
                  'museo/index.html',
                  {'museos': museos})