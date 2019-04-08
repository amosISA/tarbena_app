from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

from .models import Contract

# Create your views here.
@login_required()
@permission_required('subvenciones.add_subvencion', raise_exception=True)
def index_contracts(request):
    contracts = Contract.objects.all().prefetch_related('type', 'contractor', 'aplic_presupuestaria').order_by('contractor', 'contractor__dni', 'date_contract')

    return render(request,
                  'contracts/index.html',
                  {'contratos': contracts})