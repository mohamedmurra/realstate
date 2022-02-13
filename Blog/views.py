from django.shortcuts import render,get_object_or_404
from .models import blog,blog_catagory
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# Create your views here.


def blog_view(request):
 posts =blog.objects.all().order_by('-created')
 p = Paginator(posts, 6)
 page_number =request.GET.get('page',1)
 try:
    page_obj = p.get_page(page_number)
 except PageNotAnInteger:
    page_obj = p.page(1)
 except EmptyPage:
    page_obj = p.page(p.page_number)
 return render(request, 'blog.html',{'page_obj':page_obj})

def blog_detail(request,slug):
 post=get_object_or_404(blog,slug=slug)
 return render(request,'blog_detail.html',{'post':post})