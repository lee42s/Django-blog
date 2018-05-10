from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from notice.models import Post,Notice_category,Word_filtering,Comment,File,Imges
from django.http import HttpResponse,HttpResponseRedirect,Http404
from notice.forms import PostForm,Notice_categoryForm,Word_filteringForm,CommentForm,FlieForm,ImgesForm,PostSearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.views import generic
from django.views.decorators.csrf import csrf_protect,requires_csrf_token,csrf_exempt
import json
from django.db.models.functions import Length
from django.db.models import Q#or 쿼리셋 사용할경우
import re #html태그 제거
# Create your views here.

def post_list(request, category):
    category1 = Notice_category.objects.all()  # gnb카티고리을 불러오는 쿼리셋
    searchForm = PostSearchForm()
    category_id = Notice_category.objects.filter(id=category)
    for list_auth in category_id:
        try :
            if request.user.is_level <= list_auth.list_auth or request.user.is_superuser == True :
                posts = Post.objects.filter(category_id=category,
                                            created_date__lte=timezone.now()).order_by('-created_date')
            else:
                return render(request, 'about.html',{'category':category1,'searchForm':searchForm})
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
    return render(request, 'notice/post_list.html', {'posts': posts,'category_id':category_id,'category':category1,'searchForm':searchForm})


def post_detail(request, pk, category):
    category1 = Notice_category.objects.all()  # gnb카티고리을 불러오는 쿼리셋
    category_id=Notice_category.objects.filter(id=category)
    searchForm = PostSearchForm()
    for detail_auth in category_id:
        try :
            if request.user.is_level <= detail_auth.detail_auth or request.user.is_superuser == True :
                post_detail = Post.objects.get(pk=pk, category=category)
                post = get_object_or_404(Post, pk=pk)
                # 파일,이미지
                files = post.file_set.all()
                imges = post.imges_set.all()
            else:
                return render(request, 'about.html',{'category':category1,'searchForm':searchForm})
        except:
            return redirect('register')
    # 댓글 페이지
    comment_post = Comment.objects.filter(post_id=pk,created_date__lte=timezone.now()).order_by('-created_date')
    paginator_comment = Paginator(comment_post, 5)
    page = request.GET.get('page')
    try:
        contacts_comment = paginator_comment.page(page)
    except PageNotAnInteger:
        contacts_comment = paginator_comment.page(1)
    except EmptyPage:
        contacts_comment = paginator_comment.page(paginator_comment.num_pages)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            word_content = Word_filtering.objects.filter(id=1, text__contains=comment.text).exists()
            if word_content == True:
                comment.author = request.user
                comment.post = post
            else:
                comment.author = request.user
                comment.post = post
                comment.save()
                return redirect('notice_detail:post_detail', pk=post.pk, category=category)
    else:
        form = CommentForm()
    return render(request, 'notice/post_detail.html',
                  {'post_detail': post_detail,'category':category1,'form': form,'comment_post':contacts_comment,'files':files, 'imges': imges,'searchForm':searchForm})


@login_required
def post_new(request,category):
    if request.user.is_authenticated :
        ctgry = category
        searchForm = PostSearchForm()
        category_id = Notice_category.objects.filter(id=ctgry)
        category1 = Notice_category.objects.all()#gnb카티고리을 불러오는 쿼리셋
        for writer_auth in category_id:
            if request.method == "POST" or request.user.is_level <= writer_auth.writer_auth  or request.user.is_superuser == True:
                form = PostForm(request.POST)
                imges = ImgesForm()
                file = FlieForm()
            else:
                return render(request, 'about.html', {'category': category1,'searchForm':searchForm})
        if form.is_valid():
            post = form.save(commit=False)
            #66,67행 글 제목과 내용  중에 비방글 내용이 존재 시 Ture을 반환한다.
            cleanr = re.compile('<.*?>')#문자타입안에html태그제거
            cleanc_html = re.sub(cleanr, '', post.content)#문자타입안에html태그제거
            cleanr_content=cleanc_html.replace(" ","")#문자안에공백제거
            word_content = Word_filtering.objects.filter(id=1,text__contains=cleanr_content).exists()
            word_subject = Word_filtering.objects.filter(id=1,text__contains=post.title).exists()
            if word_content or word_subject:
                post.author = request.user
                post.category = writer_auth
            else:
                post.author = request.user
                post.category = writer_auth
                post.save()
                # 이미지,파일
                upflis = request.FILES.getlist('file')
                for upfl in upflis:
                    file = File()
                    file.file = upfl
                    file.post = post
                    file.save()
                upimges = request.FILES.getlist('imges')
                for upim in upimges:
                    imges = Imges()
                    imges.imges = upim
                    imges.post = post
                    post.imges_check = True
                    post.save()
                    imges.save()
                return redirect('notice_detail:post_detail', pk=post.pk, category=ctgry)
        else:
            form = PostForm()
            imges = ImgesForm()
            file = FlieForm()
    return render(request, 'notice/post_edit.html', {'form':form,'category':category1,
                                                     'category_id':category_id,'file': file,'imges':imges,'searchForm':searchForm})

@login_required
def comment_remove(request, pk,comment_pk,category):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.author or request.user.is_superuser==True or request.user.is_manager == True:
         comment.delete()
    return redirect('notice_detail:post_detail', pk=pk,category=category)


@login_required
def post_edit(request,pk,category):
    post_author=Post.objects.filter(id=pk)
    category1 = Notice_category.objects.all()  # gnb카티고리을 불러오는 쿼리셋
    for username in post_author:
        if request.method == 'POST' or request.user.id == username.author_id or request.user.is_manager == True or request.user.is_superuser == True:
            category_id = Notice_category.objects.filter(id=category)
            post_edit = get_object_or_404(Post, pk=pk, category=category)
            form = PostForm(request.POST, instance=post_edit)
            searchForm = PostSearchForm()
            imges = ImgesForm()
            file = FlieForm()
        else:
            return redirect('notice_detail:post_detail', pk=username.id, category=category)
        if form.is_valid():
            # 66,67행 글 제목과 내용  중에 비방글 내용이 존재 시 Ture을 반환한다.
            cleanr = re.compile('<.*?>')  # 문자타입안에html태그제거
            cleanc_html = re.sub(cleanr, '', post_edit.content)  # 문자타입안에html태그제거
            cleanr_content = cleanc_html.replace(" ", "")  # 문자안에공백제거
            # 글제목과 내용중에 비방글을 필터링해준다.
            word_content = Word_filtering.objects.filter(id=1, text__contains=cleanr_content).exists()
            word_subject = Word_filtering.objects.filter(id=1, text__contains=post_edit.title).exists()
            if word_content or word_subject:
                post = form.save(commit=False)
                post.author = request.user
                post.title = post_edit.title
                post.content = post_edit.content
            else:
                post = form.save(commit=False)
                post.author = request.user
                post.title = post_edit.title
                post.content = post_edit.content
                post.save()
                upflis = request.FILES.getlist('file')
                for upfl in upflis:
                    file = File()
                    file.file = upfl
                    file.post = post
                    file.save()
                if Imges.objects.filter(post_id=pk).exists():
                    imges_edit = Imges.objects.get(post_id=pk)
                else:
                    imges_edit = Imges()
                upimges = request.FILES.getlist('imges')
                for upim in upimges:
                    imges = imges_edit
                    imges.imges = upim
                    imges.post = post
                    post.imges_check = True
                    post.save()
                    imges.save()
                return redirect('notice_detail:post_detail', pk=post.pk, category=category)
        else:
            form = PostForm(instance=post_edit)
    return render(request, 'notice/post_edit.html', {'form': form,'category':category1,'category_id': category_id,'file': file,'imges':imges,'searchForm':searchForm})



@login_required
def post_remove(request, pk, category):
    post_author = Post.objects.filter(id=pk)
    for username in post_author:
        if request.user.id == username.author_id or request.user.is_manager == True or request.user.is_superuser == True:
            post = get_object_or_404(Post, pk=pk, category=category)
            post.delete()
        else:
            return redirect('notice_detail:post_detail', pk=pk, category=category)
    return redirect('notice_list:post_list', category=category)

@login_required
def imges_remove(request, imge_pk, pk, category):
    post_author = Post.objects.filter(id=pk)
    for username in post_author:
        if request.user.id == username.author_id or request.user.is_manager == True or request.user.is_superuser == True:
            imge=get_object_or_404(Imges, id=imge_pk)
            post=get_object_or_404(Post, id=pk)
            post.imges_check=False
            post.save()
            imge.delete()
        else:
            return redirect('notice_list:post_list', category=category)
        return redirect('notice_detail:post_detail', pk=pk, category=category)

@login_required
def files_remove(request,file_pk,pk, category):
    post_author = Post.objects.filter(id=pk)
    for username in post_author:
        if request.user.id == username.author_id or request.user.is_manager == True or request.user.is_superuser == True:
            file=get_object_or_404(File,id=file_pk)
            file.delete()
        else:
            return redirect('notice_list:post_list', category=category)
    return redirect('notice_detail:post_detail', pk=pk, category=category)

@login_required
def notice_category_manager(request):
    if request.user.is_manager == False and request.user.is_superuser == False :
        return render(request, 'about.html')
    if request.user.is_authenticated or request.user.is_manager == True or request.user.is_superuser == True:
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
    if request.user.is_manager == False and request.user.is_superuser == False:
        return render(request, 'about.html')
    if request.user.is_authenticated or request.user.is_manager == True or request.user.is_superuser == True:
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
    if request.user.is_authenticated or request.user.is_manager == True or request.user.is_superuser == True:
        category = get_object_or_404(Notice_category, pk=pk)
    if request.user.is_manager == False and request.user.is_superuser == False:
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
    if request.user.is_authenticated or request.user.is_manager == True or request.user.is_superuser == True:
        category = get_object_or_404(Notice_category, pk=pk)
        category.delete()
    if request.user.is_manager == False and request.user.is_superuser == False:
        return render(request, 'about.html')
    return redirect('m_category_list:category_list')

@login_required
def word_filtering(request):
    if request.user.is_authenticated or request.user.is_manager == True or request.user.is_superuser == True:
        word_filtering= get_object_or_404(Word_filtering,)
    if request.user.is_manager == False and request.user.is_superuser == False:
        return render(request, 'about.html')
    if request.method == 'POST':
        form = Word_filteringForm(request.POST, instance=word_filtering)
        if form.is_valid():
            word_filtering = form.save(commit=False)
            word_filtering.text = word_filtering.text
            word_filtering.save()
            return redirect('word_filtering_manager:word_filtering')
    else:
        form = Word_filteringForm(instance=word_filtering)
        return render(request, 'notice/word_filtering_edit.html',{'form': form})


@csrf_exempt
def ajax_word_filtering(request):
    post_subject= request.POST.get('subject')
    post_content= request.POST.get('content')
    cleanr = re.compile('<.*?>')  # 문자타입안에html태그제거
    cleanc_html = re.sub(cleanr, '', post_content)  # 문자타입안에html태그제거
    cleanr_content = cleanc_html.replace("\n", "")  # 엔터값제거
    data={
        'is_taken_subject': Word_filtering.objects.filter(text__contains=post_subject).exists(),
        'is_taken_content': Word_filtering.objects.filter(text__contains=cleanr_content).exists(),
    }
    if data['is_taken_subject']:
        data['error_message'] = '가 포함되어있습니다'
    if data['is_taken_content']:
        data['error_message'] = '가 포함되어있습니다'
    return JsonResponse(data)


def ajax_comment_word_filtering(request):
    comment_text = request.GET.get('comment')
    data={
         'is_taken_comment': Word_filtering.objects.filter(text__contains=comment_text).exists(),
    }
    if data['is_taken_comment']:
        data['error_message'] = '가 포함되어있습니다'

    return JsonResponse(data)

@csrf_exempt
def ajax_comment_edit(request):
    comment_id = request.POST.get('comment_id')
    number_comment_id=int(comment_id)
    comment = request.POST.get('comment')
    comment_edit=Comment.objects.get(id= number_comment_id)
    comment_edit.text = comment
    comment_edit.save()
    data={
        # 'comment_edit_text':comment_edit.text,
        'result':True
    }
    return JsonResponse(data)



def post_search(request):
    if 'search_word' in request.POST and request.POST.get('search_word'):
        sWord = request.POST.get('search_word','')
        post=Post.objects.all()
        results = post.filter(title__icontains=sWord).distinct()
        searchForm = PostSearchForm()
        category1 = Notice_category.objects.all()  # gnb카티고리을 불러오는 쿼리셋
    return render(request, 'notice/post_search_list.html', {'results': results,'query': sWord,'searchForm':searchForm,'category':category1})
