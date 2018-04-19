from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from notice.models import Post,Notice_category
from django.http import HttpResponse,HttpResponseRedirect,Http404
from notice.forms import PostForm,Notice_categoryForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.http import JsonResponse
# Create your views here.

#django-el-pagination사용
def post_list(request):
    category_title = Notice_category.objects.filter(id=request.GET.get('category'))
    for list_auth in category_title:
        try :
            if request.user.is_level <= list_auth.list_auth:
                posts = Post.objects.filter(category_id=request.GET.get('category'),
                                            created_date__lte=timezone.now()).order_by('-created_date')
            else:
                return render(request, 'about.html')
        except:
            return redirect('register')
    category =Notice_category.objects.all()#gnb카티고리을 불러오는 쿼리셋
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'notice/post_list.html', {'posts': posts,'category_title':category_title,'category':category,})


def post_detail(request,pk,category):
    category_id=Notice_category.objects.filter(id=category)
    for detail_auth in category_id:
        try :
            if request.user.is_level <= detail_auth.detail_auth:
                post_detail = Post.objects.get(pk=pk)
            else:
                return render(request, 'about.html')
        except:
            return redirect('register')
    category1 = Notice_category.objects.all()
    return render(request, 'notice/post_detail.html', {'post_detail': post_detail,'category':category1})


@login_required
def post_new(request):
    if request.user.is_authenticated or request.user.is_manager == True :
        ctgry = request.GET.get('category')
        request.session['category'] = ctgry
        category = Notice_category.objects.all()#gnb카티고리을 불러오는 쿼리셋
        category_id = Notice_category.objects.filter(id=ctgry)
        for writer_auth in category_id:
            if request.method == "POST" and request.user.is_level <= writer_auth.writer_auth:
                form = PostForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.author = request.user
                    post.save()
                    return redirect('notice_detail:post_detail',pk=post.pk,category =request.session['category'])

            if not request.user.is_level <= writer_auth.writer_auth:
                return render(request, 'about.html')
            else:
                form = PostForm()
    return render(request, 'notice/post_edit.html', {'form':form,'category':category,'category_id':category_id})

@login_required
def post_edit(request,pk,category):
    post_author=Post.objects.filter(id=pk)
    for username in post_author:
        if  request.user.id == username.author_id or request.user.is_manager==True:
            post_edit = get_object_or_404(Post, pk=pk,category=category)
        else:
            return redirect('notice_detail:post_detail', pk=username.id,category=category)
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post_edit)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.category =post_edit.category
                post.title=post_edit.title
                post.content=post_edit.content
                post.save()
                return redirect('notice_detail:post_detail', pk=post.pk,category=category)
        else:
            form = PostForm(instance=post_edit)
    return render(request, 'notice/post_edit.html',{'form':form})



@login_required
def notice_category_manager(request):
    if request.user.is_manager == False  :
        return render(request, 'about.html')
    if request.user.is_authenticated or request.user.is_manager == True:
        category_list =Notice_category.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
        category=Notice_category.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(category_list, 5)
        try:
            category_list = paginator.page(page)
        except PageNotAnInteger:
            category_list = paginator.page(1)
        except EmptyPage:
            category_list = paginator.page(paginator.num_pages)
    return render(request, 'notice/notice_category_list.html',{'category_list':category_list,'category':category })








@login_required
def new_notice_category_manager(request):
    if request.user.is_manager == False:
        return render(request, 'about.html')
    if request.user.is_authenticated or request.user.is_manager == True:
        if request.method == "POST":
            form = Notice_categoryForm(request.POST)
            if form.is_valid():
                new_category = form.save(commit=False)
                new_category.author = request.user
                new_category.save()
                return redirect('m_category_list:category_list')
        else:
            form = Notice_categoryForm()
    return render(request, 'notice/notice_category_edit.html', {'form': form})

@login_required
def notice_category_edit(request, pk):
    if request.user.is_authenticated:
        category = get_object_or_404(Notice_category, pk=pk)
    if request.user.is_manager == False:
        return render(request, 'about.html')
    if request.method == 'POST':
        form = Notice_categoryForm(request.POST, instance=category)
        if form.is_valid():
            notice_category= form.save(commit=False)
            notice_category.title=category.title
            notice_category.list_auth=category.list_auth
            notice_category.detail_auth=category.detail_auth
            notice_category.writer_auth=category.writer_auth
            notice_category.save()
            return redirect('m_category_list:category_list')
    else:
        notice_category_pk = Notice_category.objects.filter(id=pk)
        form = Notice_categoryForm(instance=category)
    return render(request, 'notice/notice_category_edit.html',{'form':form, 'notice_category_pk':notice_category_pk})

@login_required
def notice_category_remove(request, pk):
    if request.user.is_authenticated and request.user.is_manager == True:
        category = get_object_or_404(Notice_category, pk=pk)
        category.delete()
    if request.user.is_manager == False:
        return render(request, 'about.html')
    return redirect('m_category_list:category_list')


