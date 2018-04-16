from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from notice.models import Post,Notice_category
from django.http import HttpResponse,HttpResponseRedirect,Http404
from notice.forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def post_list(request):
    ctgry = request.GET['category']
    page = request.GET.get('page', 1)
    if ctgry != '':
        posts = Post.objects.filter(category__title=ctgry, created_date__lte=timezone.now()).order_by('-created_date')[:10]
        paginator = Paginator(posts, 5)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
    else:
        posts = Post.objects.all()
    category_title = Notice_category.objects.filter(title=ctgry)
    category =Notice_category.objects.all()
    return render(request, 'notice/post_list.html', {'posts': posts,'category_title':category_title,'category':category,'pages': pages})


def post_detail(request, pk):
    post_detail = Post.objects.get(pk=pk)
    return render(request, 'notice/post_detail.html', {'post_detail': post_detail})



@login_required
def post_new(request):
    category = Notice_category.objects.all()
    if request.user.is_manager == False and request.user.is_member == False:
        error = "접근 권한이 없습니다. 관리자에게 문의 하세요"
        return HttpResponse(error)
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