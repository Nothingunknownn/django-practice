from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView


from .forms import *
from .models import *
from .utils import *


class VideoCardHome(DataMixin, ListView):  # класс представления
    model = VideoCard
    template_name = 'video_card/index.html'
    context_object_name = 'posts'  # чтобы в шаблоне проходила колекция posts

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        # dict(list(context.items()) + list(c_def.items()))
        return context | c_def

    def get_queryset(self):
        return VideoCard.objects.filter(is_published=True).select_related('cat')


# def index(request):
#     posts = VideoCard.objects.all()
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#
#     return render(request, 'video_card/index.html', context=context)


def about(request):
    contact_list = VideoCard.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'video_card/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'video_card/addpage.html'
    success_url = reverse_lazy('home')  # После создания перенаправляет на глвыную страницу
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление товара")
        return context | c_def


# def add_page(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #  print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#
#     else:
#         form = AddPostForm()
#     return render(request, 'video_card/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


def market(request):
    return HttpResponse("Магазин с товарами")


def favourite(request):
    return HttpResponse("Избранное")

# def feedback(request):
#     return HttpResponse("Обратная связь")


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'video_card/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return context | c_def

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


def login(request):
    return HttpResponse("Авторизация")


class ShowPost(DataMixin, DetailView):
    model = VideoCard
    template_name = 'video_card/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return context | c_def


# def show_post(request, post_slug):
#     post = get_object_or_404(VideoCard, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id
#     }
#
#     return render(request, 'video_card/post.html', context=context)


class VideoCardCategory(DataMixin, ListView):  # класс представления
    model = VideoCard
    template_name = 'video_card/index.html'
    context_object_name = 'posts'  # чтобы в шаблоне проходила колекция posts
    allow_empty = False  # если на странице пусто, то вызывает исключение 404

    def get_queryset(self):
        return VideoCard.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return context | c_def


# def show_category(request, cat_slug):
#     cat = Category.objects.filter(slug=cat_slug)
#     posts = VideoCard.objects.filter(cat_id=cat[0].id)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat[0].id
#     }
#
#     return render(request, 'video_card/index.html', context=context)
#
#
def pageNotFound(request, exception):
    return HttpResponseNotFound(f"<h1>Страница не найдена</h1>")


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'video_card/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return context | c_def

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'video_card/login.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return context | c_def
    
    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')

