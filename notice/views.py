from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from notice.models import Post
from django.http import HttpResponse,HttpResponseRedirect,Http404
from notice.forms import PostForm
# Create your views here.


def post_list(request):
    posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')[:10]
    return render(request, 'notice/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post_detail = Post.objects.get(pk=pk)
    return render(request, 'notice/post_detail.html', {'post_detail': post_detail})



@login_required
def post_new(request):
    if request.user.is_manager == False and request.user.is_member == False:
        error = "접근 권한이 없습니다. 관리자에게 문의 하세요"
        return HttpResponse(error)
    if request.user.is_authenticated or request.user.is_manager == True or request.user.is_member == True:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.modified_date = timezone.now()
                post.save()
                return redirect('post:post_list')
        else:
            form = PostForm()
    return render(request, 'notice/post_edit.html', {'form':form})