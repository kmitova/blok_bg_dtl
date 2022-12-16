import logging

from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.views.generic import DetailView, UpdateView

from accounts.forms import UserCreateForm, UserLoginForm, AdminUserCreateForm, DeleteProfileForm, \
    CustomPasswordChangeForm
from core.utils import get_date_joined

UserModel = get_user_model()
logger = logging.getLogger('main')


class UserRegisterView(views.CreateView):
    model = UserModel
    form_class = UserCreateForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')


class AdminUserRegisterView(views.CreateView):
    model = UserModel
    form_class = AdminUserCreateForm
    template_name = 'accounts/register-admin.html'
    success_url = reverse_lazy('login')


class UserLoginView(auth_views.LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    next_page = reverse_lazy('home page')


class UserLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('landing page')


class ProfileDetailsView(DetailView):
    template_name = 'accounts/profile-page.html'
    model = UserModel

    def get_context_data(self, **kwargs):
        context = {}
        try:
            context = super().get_context_data(**kwargs)
            context["posts_count"] = self.object.post_set.count()
            context['is_owner'] = self.request.user == self.object
            context['blok_number'] = str(self.object.building_code)[2:]
            context['date_joined'] = get_date_joined(self.object.date_joined)
        except Exception as e:
            print(e)
            logging.debug('User does not exist')
        return context


class ProfileEditView(UpdateView):
    template_name = 'accounts/edit-profile.html'
    model = UserModel
    fields = ('first_name', 'last_name', 'email', 'apartment_number', 'username', 'profile_picture')

    def get_success_url(self):
        return reverse_lazy('profile page', kwargs={
            'pk': self.request.user.pk
        })


class DeleteProfileView(UpdateView):
    form_class = DeleteProfileForm
    template_name = 'accounts/verify-page.html'

    def get_success_url(self):
        return reverse_lazy('landing page')

    def get_object(self):
        return self.request.user



def change_password(request, pk):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Успешно променихте паролата си!')
            return redirect('home page')
        else:
            messages.error(request, 'Моля, поправете грешките.')
    else:
        form = CustomPasswordChangeForm(request.user)

    context = {
        'form': form
    }

    return render(request, 'accounts/change-password.html', context)

