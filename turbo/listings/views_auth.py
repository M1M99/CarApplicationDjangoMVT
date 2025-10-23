from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect,render


def signup(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save() # username + password
            login(request,user)
            messages.success(request,'Welcome you can create your ADV')
            return redirect('listing_list')
    else:
        form=UserCreationForm()
    return render(request,'auth/signup.html',{'form':form})