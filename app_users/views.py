from django.shortcuts import render
from app_users.forms import UserForm, UserProfileInfoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic import CreateView
from .models import UserProfileInfo, Contact
from curriculum.models import Standard,Comment,Reply
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail


def user_login(request):                                                        #needed
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)

                return HttpResponseRedirect(reverse('index'))
                # return render(request, 'curriculum/standard_list_view.html')
            else:
                return render(request, 'app_users/deactivated.html')
        else:
            return render(request, 'app_users/incorrect.html')
            # return HttpResponseRedirect(reverse('register'))

    else:
        return render(request, 'app_users/login.html')
def secretkey(request):
    if request.method == "POST":
        skey = request.POST.get('skey')



        if skey=="78667855":
            return render(request, 'app_users/explain.html')
        else:
            return render(request, 'app_users/incorrect.html')


    else:
        return render(request, 'app_users/slogin.html')

@login_required                                                                 #needed
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# Create your views here.
# def index(request):
#     return render(request,'app_users/index.html')

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()


            subject = 'eduNymous Account Created @aliet'
            message = 'Account Details' + '\n' + 'Username : ' + str(user.username)+ '\n' + 'Password : ' + str(user_form.cleaned_data.get('password1'))
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [str(user.email)]
            send_mail( subject, message, email_from, recipient_list )

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'app_users/registration.html',
                            {'registered':registered,
                             'user_form':user_form,
                             'profile_form':profile_form})

def report(request):
    
    if request.method == "POST":
        

        comment_id=request.POST.get('commentid')
        print(comment_id)
        if comment_id=='':
            return render(request,'app_users/reportedquery.html')
        try:
            comment_details = Comment.objects.get(epoch=comment_id)
            user_details = User.objects.select_related('user_profile').get(username=comment_details.author)
            comment_context={
                'mode':'Comment Queried',
                'c_lesson' :comment_details.lesson_name,
                'name': comment_details.author,
                'comment_text':comment_details.body,
                'com_id':comment_details.epoch,
                'candidate_email':user_details.email

            }

        except:
            comment_details = Reply.objects.get(reply_epoch=comment_id)
            user_details = User.objects.select_related('user_profile').get(username=comment_details.author)
            comment_context={
                'mode':'Replied Queried',
                'c_lesson' :comment_details.comment_name,
                'name': comment_details.author,
                'comment_text':comment_details.reply_body,  
                'com_id':comment_details.reply_epoch,
                'candidate_email':user_details.email

            }


        user_details = User.objects.select_related('user_profile').get(username=comment_details.author)
        
        return render(request,'app_users/reportedquery.html',comment_context)
    else:
        return render(request,'app_users/reportedquery.html')

class HomeView(TemplateView):                                                   #needed
    template_name = 'app_users/login.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        standards = Standard.objects.all()
        teachers = UserProfileInfo.objects.filter(user_type='teacher')
        context['standards'] = standards
        context['teachers'] = teachers
        context['mode'] = 'purple'
        return context
class home_view(TemplateView):                                                   #needed
    template_name = 'app_users/index.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        standards = Standard.objects.all()
        teachers = UserProfileInfo.objects.filter(user_type='teacher')
        context['standards'] = standards
        context['teachers'] = teachers
        return context

class ContactView(CreateView):
    model = Contact
    fields = '__all__'
    template_name = 'app_users/contact.html'


@login_required                                                                 #needed
def change_password(request):
    if request.method == "POST":
        update_password = request.POST.get('password')
        #user_details

        # u_details = User.objects.select_related('user_profile').get(username=request.user)
        # u_details.set_password(update_password)
        # u_details.save()
        request.user.set_password(update_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        return render(request, 'app_users/change.html',{"sucess_msg":"password updated successfully"})


    else:
        return render(request, 'app_users/change.html')
    
@login_required                                                                 #needed
def add_class(request):
    standards = Standard.objects.all()
    if request.method == "POST":
        teacher_name = request.POST.get('name')
        s = ","
        class_to_add = request.POST.get('class')
        t_details = User.objects.select_related('user_profile').get(username=teacher_name)
        s+=class_to_add
        # t_details.bio+=s
        # t_details.save()
        # print(t_details.id)
        u_details = UserProfileInfo.objects.get(user=t_details.id)
        # print(u_details.bio)
        u_details.bio +=s
        u_details.save()
        print(u_details.bio)
        return render(request, 'app_users/add_class.html',{"sucess_msg":"classes updated successfully","standards":standards})
    else:
        return render(request, 'app_users/add_class.html',{"standards":standards})