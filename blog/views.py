from django.utils import timezone
from django.shortcuts import render, get_object_or_404
# include拿東西時會用到的model
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()
    ).order_by('published_date')

    # template位置(2nd parameter) template要用的東西(3rd parameter)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # 存表單欄位的資料
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            # 儲存整個post(包含自動判斷的資料+輸入的資料)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
