from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from notice.models import Post,Notice_category
from django.http import HttpResponse,HttpResponseRedirect,Http404
from notice.forms import PostForm,Notice_categoryForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

#django-el-pagination사용
def post_list(request):
    ctgry = request.GET.get('category')
    category_title = Notice_category.objects.filter(id=ctgry)
    for list_auth in category_title:
        try :
            if request.user.is_level <= list_auth.list_auth:
                posts = Post.objects.filter(category_id=ctgry, created_date__lte=timezone.now()).order_by('-created_date')
            else:
                return HttpResponse('접근 권한이 없습니다.')
        except:
            return redirect('register')
    category =Notice_category.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'notice/post_list.html', {'posts': posts,'category_title':category_title,'category':category,})


def post_detail(request, pk):
    ctgry = request.GET.get('category')
    category_id=Notice_category.objects.filter(id=ctgry)
    # for detail_auth in category_id:
    #     try :
    #         if request.user.is_level <= detail_auth.list_auth:
    #             posts = Post.objects.filter(category_id=ctgry, created_date__lte=timezone.now()).order_by('-created_date')
    #         else:
    #             return redirect('login')
    #     except:
    #         return redirect('register')
    post_detail = Post.objects.get(pk=pk)
    category = Notice_category.objects.all()
    return render(request, 'notice/post_detail.html', {'post_detail': post_detail,'category':category})



@login_required
def post_new(request):
    if request.user.is_manager == False and request.user.is_member == False:
        return redirect('login')
    if request.user.is_authenticated or request.user.is_manager == True or request.user.is_member == True:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('post:post_detail', pk=post.pk )
        else:
            form = PostForm()
            category = Notice_category.objects.all()
    return render(request, 'notice/post_edit.html', {'form':form,'category':category,})


@login_required
def notice_category_manager(request):
    if request.user.is_manager == False  :
        return redirect('login')
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
        return redirect('login')
    if request.user.is_authenticated or request.user.is_manager == True:
        if request.method == "POST":
            form = Notice_categoryForm(request.POST)
            if form.is_valid():
                new_category = form.save(commit=False)
                new_category.author = request.user
                new_category.save()
                return redirect('notice:category_list')
        else:
            form = Notice_categoryForm()
    category = Notice_category.objects.all()
    return render(request, 'notice/notice_category_edit.html', {'form': form})

@login_required
def notice_category_edit(request, pk):
    if request.user.is_authenticated:
        category = get_object_or_404(Notice_category, pk=pk)
    if request.user.is_manager == False:
        return redirect('login')
    if request.method == 'POST':
        form = Notice_categoryForm(request.POST, instance=category)
        if form.is_valid():
            notice_category= form.save(commit=False)
            notice_category.title=category.title
            notice_category.list_auth=category.list_auth
            notice_category.detail_auth=category.detail_auth
            notice_category.writer_auth=category.writer_auth
            notice_category.save()
            return redirect('notice:category_list')
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
        return redirect('login')
    return redirect('notice:category_list')


