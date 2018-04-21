from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from notice.models import Post,Notice_category,Word_filtering
from django.http import HttpResponse,HttpResponseRedirect,Http404
from notice.forms import PostForm,Notice_categoryForm,Word_filteringForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect,requires_csrf_token
import json
from django.db.models.functions import Length

# Create your views here.

def post_list(request,category):
    category1 = Notice_category.objects.all()  # gnb카티고리을 불러오는 쿼리셋
    category_title = Notice_category.objects.filter(id=category)
    for list_auth in category_title:
        try :
            if request.user.is_level <= list_auth.list_auth:
                posts = Post.objects.filter(category_id=category,
                                            created_date__lte=timezone.now()).order_by('-created_date')
            else:
                return render(request, 'about.html',{'category':category1})
        except:
            return redirect('register')
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'notice/post_list.html', {'posts': posts,'category_title':category_title,'category':category1,})


def post_detail(request,pk,category):
    category1 = Notice_category.objects.all()  # gnb카티고리을 불러오는 쿼리셋
    category_id=Notice_category.objects.filter(id=category)
    for detail_auth in category_id:
        try :
            if request.user.is_level <= detail_auth.detail_auth:
                post_detail = Post.objects.get(pk=pk)
            else:
                return render(request, 'about.html',{'category':category1})
        except:
            return redirect('register')
    return render(request, 'notice/post_detail.html', {'post_detail': post_detail,'category':category1})


@login_required
def post_new(request,category):
    if request.user.is_authenticated or request.user.is_manager == True :
        ctgry = category
        category_id = Notice_category.objects.filter(id=ctgry)
        category1 = Notice_category.objects.all()#gnb카티고리을 불러오는 쿼리셋
        for writer_auth in category_id:
            if request.method == "POST" and request.user.is_level <= writer_auth.writer_auth:
                form = PostForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    #66,67행 글 제목과 내용  중에 비방글 내용이 존재 시 Ture을 반환한다.
                    word_content = Word_filtering.objects.filter(id=1,text__contains=post.content).exists()
                    word_subject = Word_filtering.objects.filter(id=1,text__contains=post.title).exists()
                    if word_content or word_subject:
                        post.title = post.content
                        post.cotent = post.title
                    else:
                        post.author = request.user
                        post.category = writer_auth
                        post.save()
                        return redirect('notice_detail:post_detail', pk=post.pk, category=ctgry)
            if not request.user.is_level <= writer_auth.writer_auth:
                return render(request, 'about.html',{'category':category1})
            else:
                form = PostForm()
    return render(request, 'notice/post_edit.html', {'form':form,'category':category1,'category_id':category_id})


@login_required
def post_edit(request,pk,category):
    post_author=Post.objects.filter(id=pk)
    category1 = Notice_category.objects.all()  # gnb카티고리을 불러오는 쿼리셋
    for username in post_author:
        if request.user.id == username.author_id or request.user.is_manager == True:
            category_id = Notice_category.objects.filter(id=category)
            post_edit = get_object_or_404(Post, pk=pk, category=category)
        else:
            return redirect('notice_detail:post_detail', pk=username.id, category=category)
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post_edit)
            if form.is_valid():
                # 66,67행 글 제목과 내용  중에 비방글 내용이 존재 시 Ture을 반환한다.
                word_content = Word_filtering.objects.filter(id=1, text__contains=post_edit.content).exists()
                word_subject = Word_filtering.objects.filter(id=1, text__contains=post_edit.title).exists()
                if word_content or word_subject:
                    return render(request, 'notice/post_edit.html',
                                  {'form': form, 'category': category1, 'category_id': category_id})
                else:
                    post = form.save(commit=False)
                    post.author = request.user
                    post.title = post_edit.title
                    post.content = post_edit.content
                    post.save()
                    return redirect('notice_detail:post_detail', pk=post.pk, category=category)
        else:
            form = PostForm(instance=post_edit)
    return render(request, 'notice/post_edit.html', {'form': form,'category':category1,'category_id': category_id})

@login_required
def post_remove(request, pk, category):
    post_author = Post.objects.filter(id=pk)
    for username in post_author:
        if request.user.id == username.author_id or request.user.is_manager == True :
            post = get_object_or_404(Post, pk=pk, category=category)
            post.delete()
        else:
            return redirect('notice_detail:post_detail', pk=pk, category=category)
    return redirect('notice_list:post_list', category=category)




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
    word_filtering=Word_filtering.objects.all()
    return render(request, 'notice/notice_category_list.html',
                  {'category_list': category_list, 'category': category,'word_filtering':word_filtering})

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

def word_filtering(request,pk):
    if request.user.is_authenticated:
        word_filtering= get_object_or_404(Word_filtering, pk=pk)
    if request.user.is_manager == False:
        return render(request, 'about.html')
    if request.method == 'POST':
        form = Word_filteringForm(request.POST, instance=word_filtering)
        if form.is_valid():
            word_filtering = form.save(commit=False)
            word_filtering.text = word_filtering.text
            word_filtering.save()
            return redirect('word_filtering_manager:word_filtering',pk=pk)
    else:
        form = Word_filteringForm(instance=word_filtering)
        return render(request, 'notice/word_filtering_edit.html',{'form': form})



def ajax_word_filtering(request):
    post_subject= request.GET.get('subject')
    post_content= request.GET.get('content')
    data={
        'is_taken_subject': Word_filtering.objects.filter(id=1,text__contains=post_subject).exists(),
        'is_taken_content': Word_filtering.objects.filter(id=1,text__contains=post_content).exists(),
    }
    if data['is_taken_subject']:
        data['error_message'] = '가 포함되어있습니다'
    if data['is_taken_content']:
        data['error_message'] = '가 포함되어있습니다'
    return JsonResponse(data)

