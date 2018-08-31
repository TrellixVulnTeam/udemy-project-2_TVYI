from django.shortcuts import render
from . import forms
from basicapp.forms import NewUserForm,UserForm,UserProfileInfoForm


# Create your views here.

def index(request):
    context_dict = {'text':'hello world','number':100}
    return render(request,'basicapp/index.html',context_dict)

def other(request):
    return render(request,'basicapp/other.html')

def relative(request):
    return render(request,'basicapp/relative_url_templates.html')



def register(request):
    registered = False

    if request.method == 'POST':
        user_form =UserForm(data =request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()


            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']


            profile.save()
            registered= True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form =UserForm()
        profile_form =UserProfileInfoForm()
    return render(request,'basicapp/registration.html',
                  {'user_form':user_form,
                   'profile_form':profile_form,
                   'registered':registered})





def form_name_view(request):
    form = forms.FormName()

    if request.method == 'POST':
        form = forms.FormName(request.POST)

        if form.is_valid():
            print("validation success!")
            print("NAME: "+form.cleaned_data['name'])
            print("EMAIL: "+form.cleaned_data['email'])
            print("TEXT: "+form.cleaned_data['text'])
    return render(request,'basicapp/form_page.html',{'form':form})

def users(request):
    form = NewUserForm()
    if request.method =="POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)

        else:
            print('ERROR FORM INVALID')

    return render(request,'basicapp/users.html',{'form':form})

