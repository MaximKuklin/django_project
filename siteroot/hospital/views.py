from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from .models import SickList, Record
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.


def get_list(request, sicklist_id):
    try:
        sicklist = SickList.objects.get(id=sicklist_id)
    except SickList.DoesNotExist:
        raise Http404(f"No such list with id={sicklist_id}")
    records = sicklist.record_set.order_by('-created_at')
    context = {'sicklist': sicklist, 'records': records}
    return HttpResponse(render(request, 'hospital/sicklist.html', context))


# @login_required(login_url='/hospital/login')
def get_sicklist(request, sicklist_id):
    render_sicklist(request, sicklist_id)


# @login_required(login_url='/hospital/login')
def get_all_lists(request):
    all_lists = SickList.objects.all()
    context = {'sicklists': all_lists}
    return HttpResponse(render(request, 'hospital/index.html', context))


def render_sicklist(request, sicklist_id, additional_context={}):
    sicklist = get_object_or_404(SickList, pk=sicklist_id)
    records = sicklist.record_set.order_by('-created_at')
    context = {'sicklist': sicklist, 'records': records, **additional_context}
    return HttpResponse(render(request, 'hospital/sicklist.html', context))


@login_required(login_url='/hospital/login')
def create_record(request, sicklist_id):
    sicklist = get_object_or_404(SickList, pk=sicklist_id)

    if sicklist.doctor_id != request.user.id:
        return HttpResponseForbidden('You can not add record here')

    error_message = None

    person = request.POST['person']
    condition = request.POST['condition']
    meds = request.POST['medicines']
    text = request.POST['text']

    if not condition or condition.isspace():
        error_message = 'Please provide non-empty patient condition!'
    elif not text or text.isspace():
        error_message = 'Please provide non-empty patient record!'
    if error_message:
        context = {'error': error_message, 'medicines': meds, 'person': person, 'condition': condition, 'text': text}
        return render_sicklist(request, sicklist_id, additional_context=context)
    else:
        Record.objects.create(sick_list=sicklist, condition=request.POST['condition'], person=person,
                              medicines=request.POST['medicines'], text=request.POST['text'])
        return HttpResponseRedirect(reverse('sicklist_by_id', kwargs={'sicklist_id': sicklist_id}))

def log_in(request):
    if request.method == 'POST':
        logout(request)
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                redirect_url = request.GET.get('next')
                if redirect_url:
                    if not user.is_staff:
                        sicklist = SickList.objects.filter(doctor_id=user.id).first()
                    else:
                        sicklist = None
                    if sicklist:
                        redirect_url = reverse('sicklist_by_id', kwargs={'sicklist_id': sicklist.id})
                    else:
                        redirect_url = reverse('index')
                return redirect(redirect_url)
            else:
                form.add_error(None, 'Invalid credentials!')
    else:
        form = LoginForm()
    return HttpResponse(render(request, 'hospital/login.html', {'form': form}))


def sign_up(request):
    if request.method == "POST":
        logout(request)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_again = form.cleaned_data['password_again']
            sicklist_title = form.cleaned_data['sicklist_title']
            user = User.objects.filter(username=username).first()
            if user is not None:
                form.add_error('username', f'User with {username} username already exists')
            elif password_again != password:
                form.add_error('password', 'Password mismatch!')
            else:
                user = User.objects.create_user(username, email, password)
                sicklist = SickList.objects.create(doctor=user, title=sicklist_title)
                login(request, user)
                return redirect(reverse('sicklist_by_id', kwargs={'sicklist_id': sicklist.id}))
    else:
        form = RegistrationForm()
    return render(request, 'hospital/singup.html', {'form': form})


def log_out(request):
    logout(request)
    redirect_url = request.GET.get('next') or reverse('index')
    return redirect(redirect_url)