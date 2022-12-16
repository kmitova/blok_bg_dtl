from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from core.utils import get_group_users, get_group_posts
from home.forms import PostCreateForm, CommentForm, ReplyForm, AnnouncementForm, PostEditForm, PostDeleteForm, \
    CommentEditForm, CommentDeleteForm, ReplyEditForm, ReplyDeleteForm
from home.models import Post, Comment, SupportPost, Notification, Reply

UserModel = get_user_model()


@login_required
def home_page(request):
    current_user = request.user
    users = get_group_users(request)
    posts = get_group_posts(request).order_by('-publication_date')
    users_count = users.count() - 1

    query = request.GET.get('query')
    query_made = False
    if query != '' and query is not None:
        posts = posts.filter(Q(user__first_name__icontains=query) |
                             Q(user__last_name__icontains=query) |
                             Q(content__icontains=query)).distinct()
        query_made = True

    context = {
        'current_user': current_user,
        'posts': posts,
        'users': users,
        'post-form': PostCreateForm(),
        'comment_form': CommentForm(),
        'reply_form': ReplyForm(),
        'query_made': query_made,
        'is_dashboard': True,
        'users_count': users_count,

    }
    return render(request, 'dashboard.html', context)


def posts_page(request):
    posts = Post.objects.filter(user=request.user).order_by('-publication_date')

    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'posts': posts,
        'comment_form': CommentForm(),
        'reply_form': ReplyForm(),
    }

    return render(request, 'partials/posts.html', context)


@login_required
def notifications_page(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-date")
    paginator = Paginator(notifications, 10)
    page = request.GET.get('page')
    notifications = paginator.get_page(page)
    for notification in notifications:
        print(notification.user.post_set.filter())
        if not notification.is_read:
            notification.is_read = True
            notification.save()

    context = {
        'notifications': notifications
    }

    return render(request, 'notifications.html', context)


def get_unread_notifications(request):
    unread_notifications = 0
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()

    context = {
        'unread_notifications': unread_notifications,
    }
    return context


def get_building_number(request):
    context = {}
    if request.user.is_authenticated:
        user = request.user
        current_building_code = user.building_code
        building_number = str(current_building_code)[2:]
        context = {
            'building_number': building_number,
        }

    return context


@login_required
def edit_post(request, post_id):
    post = Post.objects.filter(pk=post_id).get()
    if request.method == "GET":
        form = PostEditForm(instance=post)
    else:
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('posts page')

    context = {
        'form': form,
        'post_id': post_id
    }
    return render(request, 'partials/post-edit.html', context)


@login_required
def edit_comment(request, comment_id):
    comment = Comment.objects.filter(pk=comment_id).get()
    if request.method == "GET":
        form = CommentEditForm(instance=comment)
    else:
        form = CommentEditForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            comment = form.save()
            return redirect('home page')

    context = {
        'form': form,
        'comment_id': comment_id
    }
    return render(request, 'partials/comment-edit.html', context)


@login_required
def edit_reply(request, reply_id):
    reply = Reply.objects.filter(pk=reply_id).get()
    if request.method == "GET":
        form = ReplyEditForm(instance=reply)
    else:
        form = ReplyEditForm(request.POST, request.FILES, instance=reply)
        if form.is_valid():
            reply = form.save()
            return redirect('home page')

    context = {
        'form': form,
        'reply_id': reply_id
    }
    return render(request, 'partials/reply-edit.html', context)


@login_required
def delete_post(request, post_id):
    post = Post.objects.filter(pk=post_id).get()
    if request.method == "GET":
        form = PostDeleteForm(instance=post)
    else:
        form = PostDeleteForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts page')

    context = {
        'form': form,
        'post_id': post_id

    }

    return render(request, 'partials/delete-post.html', context)


@login_required
def delete_comment(request, comment_id):
    comment = Comment.objects.filter(pk=comment_id).get()
    if request.method == "GET":
        form = CommentDeleteForm(instance=comment)
    else:
        form = CommentDeleteForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('posts page')

    context = {
        'form': form,
        'comment_id': comment_id

    }

    return render(request, 'partials/delete-comment.html', context)


@login_required
def delete_reply(request, reply_id):
    reply = Reply.objects.filter(pk=reply_id).get()
    if request.method == "GET":
        form = ReplyDeleteForm(instance=reply)
    else:
        form = ReplyDeleteForm(request.POST, instance=reply)
        if form.is_valid():
            form.save()
            return redirect('posts page')

    context = {
        'form': form,
        'reply_id': reply_id

    }

    return render(request, 'partials/delete-reply.html', context)


@login_required
def delete_notification(request, notification_id):
    notification = Notification.objects.filter(pk=notification_id).get()
    notification.delete()
    return redirect('notifications')


@login_required
def comment_post(request, post_id):
    post = Post.objects.filter(pk=post_id).get()

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        if comment.user.pk != post.user.pk:
            Notification.objects.create(user=post.user,
                                        sender=comment.user,
                                        content=f"{comment.user.first_name} {comment.user.last_name} коментира вашата публикация.")

    return redirect('home page')


@login_required
def reply_to_comment(request,  post_id, comment_id):
    comment = Comment.objects.filter(pk=comment_id).get()
    post = Post.objects.filter(pk=post_id).get()

    form = ReplyForm(request.POST)
    if form.is_valid():
        reply = form.save(commit=False)
        reply.comment = comment
        reply.post = post
        reply.user = request.user
        reply.save()
        if reply.user.pk != comment.user.pk:
            Notification.objects.create(user=comment.user,
                                        sender=reply.user,
                                        content=f"{reply.user.first_name} {reply.user.last_name} отговори на вашия коментар.")

    return redirect('home page')


@login_required
def make_post(request):
    if request.method == "GET":
        form = PostCreateForm()
    else:
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()
            return redirect('home page')

    context = {
        'form': form
    }

    return render(request, 'partials/make-post.html', context)


@login_required
def make_announcement(request):
    if request.method == "GET":
        form = AnnouncementForm()
    else:
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()
            users = get_group_users(request)
            for user in users:
                if user != post.user:
                    Notification.objects.create(user=user,
                                                sender=request.user,
                                                content=f"Съобщение от вашия домоуправител: {request.user.first_name} {request.user.last_name}: "
                                                        f"{post.title}: \n "
                                                        f"{post.content}")

            return redirect('home page')

    context = {
        'form': form
    }

    return render(request, 'admin/announcement-page.html', context)


@login_required
def support_post(request, post_id):
    post = Post.objects.filter(pk=post_id).get()
    support_object = SupportPost.objects.filter(related_post_id=post_id).first()

    support = SupportPost(related_post=post)
    support.save()
    if post.user.pk != request.user.pk:
        Notification.objects.create(user=post.user,
                                    sender=request.user,
                                    content=f"{request.user.first_name} {request.user.last_name} подрепи вашата публикация.")

    return redirect(request.META['HTTP_REFERER'] + f'#{post_id}')


