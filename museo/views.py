from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404

from .models import Museo

# Create your views here.
#@login_required()
# --------------- Museo Index --------------- #
def index_museo(request):
    museos = Museo.objects.all().select_related(
        'tipus', 'classe'
        )

    return render(request,
                  'museo/index.html',
                  {'museos': museos})

# --------------- Museo Details --------------- #
def museo_detail(request, id):
    museu = get_object_or_404(Museo.objects.select_related(
                                            'tipus', 'classe'
                                        ),
                                   id=id)

    return render(request,
                  'museo/detail.html',
                  {'museu': museu})