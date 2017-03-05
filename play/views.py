from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def room(request):
    return render(request, 'room.html', {})
