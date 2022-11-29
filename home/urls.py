from django.urls import path

from home.views import home_page, notifications_page, make_post, comment_post

urlpatterns = (
    path('', home_page, name='home page'),
    path('notifications/', notifications_page, name='notifications'),
    path('make-post/', make_post, name='make post'),
    path('comment/<int:post_id>/', comment_post, name='comment post')
)