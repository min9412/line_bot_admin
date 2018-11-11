from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import LineGroupForm
from .models import LineGroup, AdminUser


# Create your views here.
def login(request):
    context = {}
    # check login
    if not request.user.is_authenticated:
        return render(request, 'line_group/login.html')


def index(request):
    context = {}
    # check login
    if not request.user.is_authenticated:
        return redirect('login')
    # check valid_user
    context['is_valid'] = AdminUser.objects.filter(
        email=request.user.email
    ).exists()
    if not context['is_valid']:
        return render(request, 'line_group/error.html')
    # get context
    context['groups'] = LineGroup.objects.all().order_by(
        'emba_group_name'
    )
    return render(request, 'line_group/index.html', context)


def select_group(request):
    context = {}
    # check login
    if not request.user.is_authenticated:
        return redirect('login')
    # check valid_user
    context['is_valid'] = AdminUser.objects.filter(
        email=request.user.email
    ).exists()
    if not context['is_valid']:
        return render(request, 'line_group/error.html')
    # get context
    line_group = request.GET.get("line_group")
    emba_group = request.GET.get("emba_group")
    groups = LineGroup.objects.all()
    if line_group:
        # 如果包含
        groups = groups.filter(line_group_name__icontains=line_group)
    if emba_group:
        groups = groups.filter(emba_group_name=emba_group)
    context['groups'] = groups.order_by('emba_group_name')
    return render(request, 'line_group/select_group.html', context)


def add_new_group(request):
    context = {}
    # check login
    if not request.user.is_authenticated:
        return redirect('login')
    # check valid_user
    context['is_valid'] = AdminUser.objects.filter(
        email=request.user.email
    ).exists()
    if not context['is_valid']:
        return render(request, 'line_group/error.html')
    # get context
    if request.method == "POST":
        # 把POST data轉成form的type
        form = LineGroupForm(request.POST)
        if form.is_valid():
            # 創造一個暫時的for; ModelForm都有的function
            group = form.save(commit=False)
            group.created_by = str(request.user)
            group.created_at = timezone.now()
            # 完成所需的修正後存到DB
            group.save()
            return redirect('select_group')
    else:
        context['form'] = LineGroupForm()
    return render(request, 'line_group/add_new_group.html', context)


# 網址裡面有參數在進到url的時候就會被拆解成request跟pk
def edit_group(request, pk):
    context = {}
    # check login
    if not request.user.is_authenticated:
        return redirect('login')
    # check valid_user
    context['is_valid'] = AdminUser.objects.filter(
        email=request.user.email
    ).exists()
    if not context['is_valid']:
        return render(request, 'line_group/error.html')
    # get context
    if request.method == "POST":
        group = LineGroup.objects.get(id=pk)
        form = LineGroupForm(request.POST, instance=group)
        if form.is_valid():
            group = form.save(commit=False)
            group.modified_by = str(request.user)
            group.modified_at = timezone.now()
            group.save()
            return redirect('select_group')
    else:
        group = LineGroup.objects.get(id=pk)
        context['form'] = LineGroupForm(instance=group)
    return render(request, 'line_group/edit_group.html', context)
