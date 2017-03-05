from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .forms import EditProfileForm, ReportForm
from register.models import UserModel

from django.shortcuts import render, redirect


# all views that require login except play because it has more
# complex logic and is a different function

@login_required
def profile(request):
    userc = request.user
    context = {
        'username': userc.username,
        'name': userc.get_full_name,
        'rank': userc.rank,
        'score': userc.score,
        'date': userc.date_joined,
        'description': userc.description,
        'country': userc.country.name,
        'country_flag': userc.country.flag,
        'img': userc.avatar_url(),
    }
    return render(request, 'profile.html', context)


@login_required
def profile_edit(request):
    instance = get_object_or_404(UserModel, id=request.user.id)
    form = EditProfileForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/edit_profile')
    context = {
        'form': form
    }
    return render(request, 'profile_edit.html', context)


@login_required
def ranklist(request):
    table = UserModel.objects.order_by('-score')
    return render(request, 'ranklist.html', {'table': table})


@login_required
def report_form(request):
    form = ReportForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("/report")
    context = {
        'form': form
    }
    return render(request, 'report.html', context)
