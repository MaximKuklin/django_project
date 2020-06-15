from django.http import HttpResponse, Http404
from .models import SickList, Record
from django.template import loader
from django.shortcuts import render, get_object_or_404
# Create your views here.


def get_list(request, list_id):
    try:
        sicklist = SickList.objects.get(id=list_id)
    except SickList.DoesNotExist:
        raise Http404(f"No such list with id={list_id}")
    records = sicklist.record_set.order_by('-created_at')
    context = {'sicklist': sicklist, 'records': records}
    return HttpResponse(render(request, 'hospital/sicklist.html', context))


def get_all_lists(request):
    all_lists = SickList.objects.all()
    context = {'sicklists': all_lists}
    return HttpResponse(render(request, 'hospital/index.html', context))


def create_record(request, sicklist_id):
    sicklist = get_object_or_404(SickList, pk=sicklist_id)
    Record.objects.create(sicklist=sicklist, condition=request.POST['condition'],
                          medicines=request.POST['medicines'])
    records = sicklist.record_set.order_by('-created_at')
    context = {'sicklist': sicklist, 'records': records}
    return HttpResponse(render(request, 'hospital/sicklist.html', context))
