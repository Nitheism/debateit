from django.shortcuts import render, redirect


# Create your views here.
def home(request):
    if request.user.is_authenticated():
        return redirect('/profile/'+request.user.username)
    return render(request, 'home.html', {})
