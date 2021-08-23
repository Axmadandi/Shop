from django.shortcuts import render, redirect
from django.views.generic.base import View
from .forms import UserRegisterForm

# Create your views here.
class RegisterView(View):

	def get(self,request):
		form = UserRegisterForm()
		return render(request, 'registration/register.html', {'form':form})

	def post(self,request):
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('main:index')
		else:
			form = UserRegisterForm()
		return render(request, 'registration/register.html', {'form':form})

def customer(request):
	user = request.user
	d = user.extra_data
	data = {
		'data':d
	}
	return render(request, 'index.html', {'data':data})