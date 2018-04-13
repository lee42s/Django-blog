from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from notice.models import Post
from django.http import HttpResponse,HttpResponseRedirect,Http404
# Create your views here.

@login_required
def manager_post_list(request):
    if request.user.is_authenticated or request.user.is_manager == True:
        if  request.user.is_manager == False:
            error = "관리자계정으로만 접근가능합니다"
            return HttpResponse(error)

    posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')[:10]
    return render(request, 'notice/manager_post_list.html', {'posts': posts})

@login_required
def manager_post_detail(request, pk):
    post_detail = Post.objects.get(pk=pk)
    return render(request, 'notice/manager_post_detail.html', {'post_detail': post_detail})