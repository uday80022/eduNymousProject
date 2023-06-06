from django.shortcuts import render
from django.views.generic import (TemplateView, DetailView,ListView, CreateView,UpdateView,DeleteView,FormView)
from .models import Standard, Subject, Lesson, Comment, WorkingDays, TimeSlots,Reply

from django.urls import reverse_lazy
from .forms import CommentForm,ReplyForm, LessonForm,SubjectForm
from django.http import HttpResponseRedirect
#nihal code
from django.db.models import Q
from django.contrib.auth.models import User
from app_users.models import UserProfileInfo
from django.views.decorators.clickjacking import xframe_options_sameorigin
import datetime
import time
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
import re
from django.http import JsonResponse
from django.views.generic import DetailView, FormView



class StandardListView(ListView):
    context_object_name = 'standards'
    model = Standard
    template_name = 'curriculum/standard_list_view.html'
    
    # def get_queryset(self):
    #     return Standard.objects.filter(name=self.request.user)
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     a = self.request.user.user_profile.bio
    #     context["user"] = a
    #     return context
class StandardLearningListView(ListView):
    # context_object_name = 'standards'
    model = Standard
    template_name = 'curriculum/learning_list_view.html'
    def get_queryset(self):
        return Standard.objects.filter(name="learningcontent")
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["standards"] = Standard.objects.all()
    #     return context
    
        

    

class SubjectListView(DetailView):
    context_object_name = 'standards'
    extra_context = {
        'slots': TimeSlots.objects.all(),
        'sem_num':['1','2','3','4','5','6','7','8'],
        
    }
    model = Standard
    template_name = 'curriculum/subject_list_view.html'

class LessonListView(DetailView):
    context_object_name = 'subjects'
    model = Subject
    template_name = 'curriculum/lesson_list_view.html'

class LessonDetailView1(DetailView):
    context_object_name = 'lessons'
    model = Lesson
    template_name = 'curriculum/lesson_nihal_view.html'
    
    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.Standard
        subject = self.object.subject
        return reverse_lazy('curriculum:lesson_detail',kwargs={'standard':standard.slug,
                                                             'subject':subject.slug,
                                                             'slug':self.object.slug})

class LessonDetailView(DetailView, FormView):
    context_object_name = 'lessons'
    model = Lesson
    template_name = 'curriculum/lesson_nihal_view.html'
    form_class = CommentForm
    second_form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        # print("hi",context)
        if 'form' not in context:
            context['form'] = self.form_class(request=self.request)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(request=self.request)
        # context['comments'] = Comment.objects.filter(id=self.object.id)
        return context
        
        
    

    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        current_time = timezone.now()
        self.epoch_time = int(current_time.timestamp())

        
        if 'form' in request.POST:
            form_class = self.get_form_class()
            # print(form_class) #<class 'curriculum.forms.CommentForm'>
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'
        
        # subject = 'Comment in Subject'
        # message = str(self.object.subject)+" "+str(self.object)+" body comment "+str(self.epoch_time) 
        # email_from = settings.EMAIL_HOST_USER
        # # print("lesson: ",self.object.id)
        # a =Lesson.objects.get(id=self.object.id) 
        # # print(a.created_by)
        # fac_mail= User.objects.select_related('user_profile').get(username=a.created_by)
        # # c_try = Comment.objects.get(epoch=self.epoch_time)
        # # print("c_try",c_try.Body)
        # # print("ki",fac_mail.email)
        
        # recipient_list = [str(fac_mail.email)]
        # # send_mail( subject, message, email_from, recipient_list )
        print(self.object) # lesson name
        print(self.object.subject) #subject name

        form = self.get_form(form_class)
        # print(form)
        # print("the form name is : ", id(2997601008320))
        # print(self.objects.get(id="2997601008320"))
        # print("form name: ", form_name)
        # print("form_class:",form_class)

        if form_name=='form' and form.is_valid():
            # print("comment form is returned")
            return self.form_valid(form)
        elif form_name=='form2' and form.is_valid():
            print("reply form is returned")
            return self.form2_valid(form)


    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.Standard
        subject = self.object.subject
        return reverse_lazy('curriculum:lesson_detail',kwargs={'standard':standard.slug,
                                                             'subject':subject.slug,
                                                             'slug':self.object.slug})
    def form_valid(self, form):
        self.object = self.get_object()
        
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.lesson_name = self.object.comments.name
        fm.lesson_name_id = self.object.id
        fm.epoch = self.epoch_time
        # print(fm.lesson_name,fm.lesson_name_id)
        # post = Comment.objects.get(id=self.object.id)
        # print(post)
        
        
        fm.save()

        #mail code final
        # subject = 'Comment'
        # comment_content = Comment.objects.get(epoch=fm.epoch)
        # message = str(self.object.subject)+"    "+str(self.object)+'    '+ str(comment_content.body)+'  ' +str(self.epoch_time) 
        # email_from = settings.EMAIL_HOST_USER
        # a =Lesson.objects.get(id=self.object.id) 
    
        # fac_mail= User.objects.select_related('user_profile').get(username=a.created_by)
       
        
        # recipient_list = [str(fac_mail.email)]
        # send_mail( subject, message, email_from, recipient_list )
        
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form):
        
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        
        fm.reply_epoch = self.epoch_time
        
        fm.save()

        # subject = 'Reply'
        # comment_content = Reply.objects.get(reply_epoch = self.epoch_time)
        # message = str(self.object.subject)+"\n"+str(self.object)+'\n'+ str(comment_content.reply_body)+'\n' +str(self.epoch_time) 
        # email_from = settings.EMAIL_HOST_USER
        # a =Lesson.objects.get(id=self.object.id) 
    
        # fac_mail= User.objects.select_related('user_profile').get(username=a.created_by)
        # cand_email=User.objects.select_related('user_profile').get(username=comment_content.author)
        # # print(cand_email.email)
        
        # recipient_list = [str(fac_mail.email)]
        # send_mail( subject, message, email_from, recipient_list )
        # main_comment = Comment.objects.get(id = fm.comment_name_id).body
        # main_comm_message ="Subject : "+ str(self.object.subject)+"\n"+"Lesson : "+str(self.object)+"\n"+"To comment :"+main_comment+"\n"+ "Relpy is : "+str(comment_content.reply_body)
        # send_mail('Replied to your Comment',main_comm_message,email_from,[str(cand_email.email)])

        return HttpResponseRedirect(self.get_success_url())


class SubjectCreateListView(CreateView):
    # fields = ('lesson_id','name','position','image','video','ppt','Notes')
    form_class = SubjectForm
    context_object_name = 'standard'
    model= Standard
    template_name = 'curriculum/subject_create.html'

    def get_success_url(self):
        self.object = self.get_object()
        self.object = str(self.object).lower()
        return reverse_lazy('curriculum:subject_list',kwargs={'slug':self.object})


    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        # fm.created_by = self.request.user
        # fm.Standard = self.object()
        # fm.subject = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

class LessonCreateView(CreateView):
    # fields = ('lesson_id','name','position','image','video','ppt','Notes')
    form_class = LessonForm
    context_object_name = 'subject'
    model= Subject
    template_name = 'curriculum/lesson_create.html'

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.standard
        return reverse_lazy('curriculum:lesson_list',kwargs={'standard':standard.slug,
                                                             'slug':self.object.slug})

    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.Standard = self.object.standard
        fm.subject = self.object

        video = form.cleaned_data['video']
        # if "youtu.be" in video:
        #     s = video.split("/")
        #     fm.video = s[3]
        # else:
        #     s = video.split("v=")[1]
        #     if "&" in s:
        #         s = s.split("&")[0]
        #         fm.video = s
        #     fm.video = s

        video_id = None 
        if "youtu.be" in video:
            s = video.split("/")
            video_id = s[3]
        else:
            s = re.findall(r"v=([^&]+)", video)
            if s:
                video_id = s[0]
            fm.video = video_id
        # # https://www.youtube.com/embed/iZ5my3krEVM

        fm.save()
        return HttpResponseRedirect(self.get_success_url())

class LessonUpdateView(UpdateView):
    fields = ('name','position','video','ppt','Notes')
    model= Lesson
    template_name = 'curriculum/lesson_update.html'
    context_object_name = 'lessons'
    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        # fm.created_by = self.request.user
        # fm.Standard = self.object.standard
        # fm.subject = self.object

        #nihal code
        video = form.cleaned_data['video']
        video_id = None 
        if "youtu.be" in video:
            s = video.split("/")
            video_id = s[3]
        else:
            s = re.findall(r"v=([^&]+)", video)
            if s:
                video_id = s[0]
            fm.video = video_id 

        # https://www.youtube.com/embed/iZ5my3krEVM
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

class LessonDeleteView(DeleteView):
    model= Lesson
    context_object_name = 'lessons'
    template_name = 'curriculum/lesson_delete.html'

    def get_success_url(self):
        print(self.object)
        standard = self.object.Standard
        subject = self.object.subject
        return reverse_lazy('curriculum:lesson_list',kwargs={'standard':standard.slug,'slug':subject.slug})
