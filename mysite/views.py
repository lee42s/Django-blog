from django.views.generic.base import TemplateView
from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from mysite.forms import CreateUserForm
from django.contrib.auth import login
from django.contrib.auth import forms as auth_forms
from django import forms
from member.models import User
from notice.models import Post,Notice_category,Imges
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.views import PasswordChangeDoneView,PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from notice.forms import PostSearchForm
from django.db.models import Q

def home(request):
    category = Notice_category.objects.all()  # gnb카티고리을 불러오는 쿼리셋
    category_title=['공지사항','자유게시판','겔러리게시판','Django','less','HTML','javascript','NORMAL-회원게시판']
    for category_title in category_title:
        if category_title == '공지사항':
            category_id1 = Notice_category.objects.filter(title=category_title)
        if  category_title == '자유게시판':
            category_id2 = Notice_category.objects.filter(title=category_title)
        if category_title == '겔러리게시판':
            category_id3 = Notice_category.objects.filter(title=category_title)
        if category_title == 'Django':
            category_id4 = Notice_category.objects.filter(title=category_title)
        if category_title == 'less':
            category_id5 = Notice_category.objects.filter(title=category_title)
        if category_title == 'HTML':
            category_id6 = Notice_category.objects.filter(title=category_title)
        if category_title == 'javascript':
            category_id7 = Notice_category.objects.filter(title=category_title)
        if category_title == 'NORMAL-회원게시판':
            category_id8 = Notice_category.objects.filter(title=category_title)
    posts1 = Post.objects.filter(category=category_id1,created_date__lte=timezone.now()).order_by('-created_date')[:5]#공지사항
    posts2 = Post.objects.filter(category=category_id2, created_date__lte=timezone.now()).order_by('-created_date')[:5]#자유게시판
    posts3 = Post.objects.filter(category=category_id3, created_date__lte=timezone.now()).order_by('-created_date')[:5]#겔러리게시판
    posts4 = Post.objects.filter(category=category_id4, created_date__lte=timezone.now()).order_by('-created_date')[:5]#Django
    posts5 = Post.objects.filter(category=category_id5, created_date__lte=timezone.now()).order_by('-created_date')[:5]#less
    posts6 = Post.objects.filter(category=category_id6, created_date__lte=timezone.now()).order_by('-created_date')[:5]#HTML
    posts7 = Post.objects.filter(category=category_id7, created_date__lte=timezone.now()).order_by('-created_date')[:5]#javascript
    posts8 = Post.objects.filter(category=category_id8, created_date__lte=timezone.now()).order_by('-created_date')[:5]#비회원게시판
    imges = Imges.objects.filter(post_id=posts3)[:5]
    searchForm = PostSearchForm()
    return render(request, 'home.html',{'posts1': posts1,'posts2': posts2,'posts3': posts3,'posts4': posts4,'posts5': posts5,
                                    'posts6': posts6,'posts7': posts7,'posts8': posts8,'category': category ,'imges':imges,'searchForm':searchForm})

@login_required
def admin_home(request):
    if request.user.is_authenticated or request.user.is_superuser == True or request.user.is_manager ==True:
        if request.user.is_manager ==False and request.user.is_superuser == False:
            return redirect('login')
    user_is_member=User.objects.filter(is_member=True,is_manager=False,is_superuser=False,date_joined__lte=timezone.now()).order_by('-date_joined')
    none_user = User.objects.filter(is_member=False,is_manager=False,is_superuser=False,date_joined__lte=timezone.now()).order_by('-date_joined')
    user_is_manager = User.objects.filter(Q(is_manager=True)|Q(is_superuser=True),date_joined__lte=timezone.now()).order_by('-date_joined')
    posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')

    category = Notice_category.objects.all()#gnb카티고리을 불러오는 쿼리셋
    #paginator_is_member
    paginator_is_member = Paginator(user_is_member, 5)
    page = request.GET.get('page')
    try:
        contacts_is_member = paginator_is_member.page(page)
    except PageNotAnInteger:
        contacts_is_member = paginator_is_member.page(1)
    except EmptyPage:
        contacts_is_member = paginator_is_member.page(paginator_is_member.num_pages)
    # paginator_none_user
    paginator_none_user = Paginator(none_user, 5)
    page_none_user = request.GET.get('page')
    try:
        contacts_none_user = paginator_none_user.page(page_none_user)
    except PageNotAnInteger:
        contacts_none_user = paginator_none_user.page(1)
    except EmptyPage:
        contacts_none_user = paginator_none_user.page(paginator_none_user.num_pages)

    #paginator_is_manager
    paginator_user_is_manager = Paginator(user_is_manager, 5)
    page_is_manager = request.GET.get('page')
    try:
        contacts_is_manager = paginator_user_is_manager.page(page_is_manager)
    except PageNotAnInteger:
        contacts_is_manager = paginator_user_is_manager.page(1)
    except EmptyPage:
        contacts_is_manager = paginator_user_is_manager.page(paginator_user_is_manager.num_pages)

    paginator_posts = Paginator(posts, 5)
    page_post = request.GET.get('page')
    try:
        contacts_post = paginator_posts.page(page_post)
    except PageNotAnInteger:
        contacts_post = paginator_posts.page(1)
    except EmptyPage:
        contacts_post = paginator_posts.page(paginator_posts.num_pages)
    return render(request,'manager/home.html', {'user_is_member':contacts_is_member,'none_user':contacts_none_user,
                                                'user_is_manager':contacts_is_manager,
                                                'posts':contacts_post,'category': category})



class UserRegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('home')
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['category'] = Notice_category.objects.all()
        context['searchForm']=PostSearchForm()
        return context

class UserPasswordChangeView(PasswordChangeView,):

    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change_form.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['category'] = Notice_category.objects.all()#gnb카티고리을 불러오는 쿼리셋
        context['searchForm'] = PostSearchForm()
        return context


class UserPasswordDoneView(PasswordChangeDoneView,):
     template_name = 'registration/password_change_done.html'
     def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['category'] = Notice_category.objects.all()#gnb카티고리을 불러오는 쿼리셋
        context['searchForm'] = PostSearchForm()
        return context



# get 방식
def validate_username(request):
    # HttpRequest 객체의 GET 과 POST 속성은 django.http.QueryDict 의 인스턴스입니다.
    # get()메서드는 키(여기서는 username)이 없는 경우 기본값 'None'을 반환합니다. https://goo.gl/wtA6KN
    username = request.GET.get('username', None)
    data = {
        # <필드명>__iexact는 대소문자를 구분하지 않고 일치하는 값을 찾는다. https://goo.gl/5XywcT
        # exists()는 쿼리셋에 결과가 있는 경우 True를 반환합니다. https://goo.gl/Vgtr2u
        'is_taken_username':User.objects.filter(username__iexact = username).exists()
    }
    if data['is_taken_username']:
        data['error_message'] = '아이디가 이미 존재합니다. 다른 이름을 입력해 주세요.'
    # data를 Json형식으로 인코딩되도록 합니다.
    return JsonResponse(data)

