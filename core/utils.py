from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import password_validators_help_texts
from django.utils.html import format_html, format_html_join

from home.models import Post


def get_date_joined(date):
    current_date = date
    current_date_no_time = current_date.strftime('%d.%m.%Y')
    return current_date_no_time


UserModel = get_user_model()


def get_building_code(request):
    current_user = request.user
    current_building_code = current_user.building_code
    return current_building_code


def get_group_posts(request):
    current_building_code = get_building_code(request)
    posts = Post.objects.filter(user__building_code=current_building_code)
    return posts


def get_group_users(request):
    current_building_code = get_building_code(request)
    users = UserModel.objects.filter(building_code=current_building_code)
    return users


def change_password_help_text(password_validators=None):
    help_texts = ["Вашата парола не може да бъде твърде подобна на другата ви лична информация.",
                  "Вашата парола трябва да съдържа поне 8 знака.",
                  "Вашата парола не може да бъде често използвана парола.",
                  "Вашата парола не може да бъде изцяло цифрова."
                  ]
    help_items = format_html_join(
        "", "<li>{}</li>", ((help_text,) for help_text in help_texts)
    )
    return format_html("<ul>{}</ul>", help_items) if help_items else ""
