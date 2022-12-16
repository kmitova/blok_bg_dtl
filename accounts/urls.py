from django.urls import path, include

from accounts.views import UserRegisterView, UserLoginView, UserLogoutView, AdminUserRegisterView, \
 ProfileDetailsView, ProfileEditView, change_password, DeleteProfileView

urlpatterns = (
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register-admin/', AdminUserRegisterView.as_view(), name='register admin'),
    path('profile/<int:pk>/', include([
        path('', ProfileDetailsView.as_view(), name="profile page"),
        path('change-password/', change_password, name='change password'),

        path('edit/', ProfileEditView.as_view(), name="edit profile"),
        path('delete/', DeleteProfileView.as_view(), name="delete profile"),

    ])),
    # path('change-password/', change_password, name='change password'),
)
