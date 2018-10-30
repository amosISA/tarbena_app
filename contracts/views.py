from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

from .models import Contract

# Create your views here.
@login_required()
@permission_required('subvenciones.can_add_subvencion', raise_exception=True)
def index_contracts(request):
    contracts = Contract.objects.all().extra(
        select={'myinteger': 'CAST(identificador AS INTEGER)'}
    ).order_by('myinteger')

    return render(request,
                  'contracts/index.html',
                  {'contratos': contracts})