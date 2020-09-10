from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .forms import CommentForm

from taggit.models import Tag


def post_list(request, tag_slug=None):
    """The function displays the main page of our blog.
    It retrieves all published posts from the database and
    shows them on the page. There is tag system and pagination"""
    object_list = Post.published_posts.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html',
                  {'posts': posts, 'page': page, 'tag': tag})


def post_detail(request, year, month, day, post):
    """This function renders post's page to the template detail.html.
        Retrieves all the comments from the database and accepts comments
        from users"""
    post = get_object_or_404(Post, slug=post,
                             status='published', published__year=year,
                             published__month=month, published__day=day)

    comments = post.comments.filter(active=True)
    ten_last_comments = comments[:10]

    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return HttpResponseRedirect(reverse('blog:post_detail', args=[post.published.year,
                                                post.published.month,
                                                post.published.day, post.slug]))
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html',
                  {'post': post, 'ten_last_comments': ten_last_comments,
                   'comments': comments, 'new_comment': new_comment,
                   'comment_form': comment_form})


class Register(CreateView):
    """The function creating and displaying form for users
    registration."""
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)




