from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from .models import Item,Sell

def home(request):
    item_list=Item.objects.all()
    sell=sell_list=Sell.objects.all()
    total=sum(sell.values_list('pprice',flat=True))
    vat=total*15/100
    context={
        'item_list':item_list,
        'total':total,
        'vat':vat,
    }
    return render(request, 'users/home.html',context)


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

def product(request):
    item_list=Item.objects.all()
    context={
        'item_list':item_list
    }
    return render(request,'users/product.html',context)

def additem(request):
    if request.method=="POST":
        name=request.POST['name']
        brandname=request.POST['brandname']
        price=request.POST['price']
        describe=request.POST['describe']
        item=Item(name=name,brandname=brandname,price=price,describe=describe)
        item.save()
        messages.info(request,"Item Added Successfully")
    else:
        pass

    item=item_list=Item.objects.all()
    context={
        'item_list':item_list
    }
    return render(request,'users/addproduct.html',context)


def delete_item(request,myid):
    item=Item.objects.get(id=myid)
    item.delete()
    messages.info(request,"Product Deleted Successfully")
    return redirect(to='users-additem')

def edit_item(request,myid):
    sel_item=Item.objects.get(id=myid)
    item_list=Item.objects.all()
    context={
        'sel_item':sel_item,
        'item_list':item_list
    }
    return render(request,'users/addproduct.html',context)

def update_item(request,myid):
    item=Item.objects.get(id=myid)
    item.name=request.POST['name']
    item.brandname=request.POST['brandname']
    item.price=request.POST['price']
    item.describe=request.POST['describe']
    item.save()
    messages.info(request,"Udate Successfully")
    return redirect(to='users-additem')


def sellitem(request):
    if request.method=="POST":
        pname=request.POST['pname']
        pprice=request.POST['pprice']
        date=request.POST['date']
        sell=Sell(pname=pname,pprice=pprice,date=date)
        sell.save()
        messages.info(request,"Sell Record Saved SuccessFully")
    else:
        pass

    sell=sell_list=Sell.objects.all()
    context2={
        'sell_list':sell_list,
    }
    return render(request,'users/sellproduct.html',context2)

def delete_sell(request,myid):
    sell=Sell.objects.get(id=myid)
    sell.delete()
    messages.info(request,"Sell Record Deleted")
    return redirect(to='users-sellitem') 


def help(request):
    return render(request,'users/help.html')

def brand(request):
    return render(request,'users/brand.html')

def vendor(request):
    return render(request,'users/vendor.html')

def order(request):
    return render(request,'users/order.html')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})


