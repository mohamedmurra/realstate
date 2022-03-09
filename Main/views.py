from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import House,City, aria,galary,extras,Building,Contact
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth import authenticate ,login ,logout
from .forms import AuthenticationForm,UserUpdateForm,register_form,house_form,glary_form,extra_form,contact_form
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from Acounnt.models import Acount
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from Blog.models import blog
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from Blog.forms import blog_form
from Blog.models import blog



def homepage(request):
  building = Building.objects.all()
  houses =House.objects.all().order_by('-created')
  house_cro =House.objects.all().order_by('created')[:3]
  agents =Acount.objects.all()
  Aria =aria.objects.all()
  posts =blog.objects.all().order_by('-created')[:4]
  return render(request, 'index.html', {'houses': houses, 'house_cro': house_cro, 'agents': agents, 'Aria': Aria, 'posts': posts, 'building': building})

def propertes(request):
  building = House.objects.filter(status=True)
  typ = request.GET.get('type')
  Aria =aria.objects.all()

  if typ == 'للأيجار':
    houses = House.objects.filter(property_type='للأيجار').order_by('-created')
  elif typ == 'للبيع':
    houses = House.objects.filter(property_type='للبيع').order_by('-created')
  else :
      houses = House.objects.all().order_by('-created')
  p = Paginator(houses, 6)
  page_number =request.GET.get('page',1)
  try:
    page_obj = p.get_page(page_number)
  except PageNotAnInteger:
    page_obj = p.page(1)
  except EmptyPage:
    page_obj = p.page(p.page_number)
  return render(request, 'property-grid.html', {'page_obj': page_obj, 'Aria': Aria, 'building': building})

def property_detail(request,slug):
  building = Building.objects.all()
  Aria =aria.objects.all()
  house =get_object_or_404(House,slug=slug)
  images =galary.objects.filter(proper=house)
  extra =extras.objects.filter(proper=house)
  return render(request,'property-single.html',{'house':house,'images':images,'extras':extra,'Aria':Aria,'building':building})

def login_view(request):
  Aria =aria.objects.all()
  if request.user.is_authenticated:
    return redirect('homepage')
  else:
    if request.POST:
      form = AuthenticationForm(request.POST)
      if form.is_valid():
        email =form.cleaned_data.get('email')
        password =form.cleaned_data.get('password')
        user =authenticate(email=email ,password=password)
        if user:
               login(request, user)
               return redirect('homepage')
    else:
      form=AuthenticationForm()
  return render(request,'login.html',{'form':form,'Aria':Aria}) 

def register_view(request):
  Aria =aria.objects.all()
  if request.user.is_authenticated:
    return redirect('homepage')
  else:
    if request.POST:
      form = register_form(request.POST)
      if form.is_valid():
        form.save()
        return redirect('login')
    else:
      form =register_form()
  return render(request,'register.html',{'form':form,'Aria':Aria}) 

def logout_view(request):
   logout(request)
   return redirect('homepage')

def agent(request,slug):
  building = Building.objects.all()
  agent =get_object_or_404(Acount,email=slug)
  houses =House.objects.filter(Agent=agent)
  Aria =aria.objects.all()
  return render(request,'agent_detail.html',{'agent':agent,'houses':houses,'Aria':Aria,'building':building,'count':houses.count()})

def agents(request):
  building = Building.objects.all()
  agents =Acount.objects.all()
  Aria =aria.objects.all()
  p = Paginator(agents, 6)
  page_number =request.GET.get('page',1)
  try:
    page_obj = p.get_page(page_number)
  except PageNotAnInteger:
    page_obj = p.page(1)
  except EmptyPage:
    page_obj = p.page(p.page_number)
  return render(request,'agent.html',{'agents':page_obj,'Aria':Aria,'building':building})


def about(request):
  building = Building.objects.all()
  team =Acount.objects.all()
  Aria =aria.objects.all()
  return render(request, 'about.html', {'team':team,'Aria':Aria,'building':building})

def contact(request):
  form =contact_form()
  building = Building.objects.all()
  Aria =aria.objects.all()
  if request.method == 'POST':
    form =contact_form(request.POST)
    if form.is_valid():
        subject='my websity'
        body ={
        'name' : form.cleaned_data['name'],
        'subject' : form.cleaned_data['subject'],
        'from_mail' : form.cleaned_data['email'],
        'messaage' : form.cleaned_data['messaage'],
        }
        message ='\n'.join(body.values())
        try:
            send_mail(subject, message, 'mohamedmura1995@gmail.com',['admin@gmail.com'])
            Contact.objects.create(
                name=body['name'], subject=body['subject'], email=body['from_mail'], messaage=body['messaage'])
            messages.success(request,'تم ارسال الرسالة بنجاح')
        except BadHeaderError:
            return HttpResponse('Invalid request')
            messages.error(request, 'لم يتم ارسال الرسالة لوجود خطأ')
  return render(request, 'contact.html', {'Aria': Aria, 'building': building, 'form': form})


def searsh_header(request):
  building = Building.objects.all()
  Aria =aria.objects.all()
  key = request.GET.get('key')
  buil = request.GET.get('building_type')
  typ =request.GET.get('type')
  ari =request.GET.get('aria')
  roms =request.GET.get('roms')
  bathrom =request.GET.get('bathrom')
  min_price =request.GET.get('min_price')
  max_price =request.GET.get('max_price')
  qs =House.objects.all()
  if key != '' and not None:
    qs = qs.filter(title__icontains=key)
  if ari != '' and not None:
    if ari != 'الكل':
      qs = qs.filter(aria__name__icontains=ari)
  if buil != '' and not None:
    if buil != 'الكل':
      qs = qs.filter(building_type__name=buil)
  if typ != '' and not None :
    if typ != 'كل العقارات':
      qs = qs.filter(property_type=typ)
  if bathrom != '' and not None:
    qs = qs.filter(bathrooms = bathrom)
  if roms != '' and not None:
    qs = qs.filter(num_rooms = roms)
  if min_price != '' and not None:
    qs =qs.filter(price__gte=min_price)
  if max_price != '' and not None:
    qs = qs.filter(price__lte=max_price)
  
  return render(request,'searsh.html',{"page_obj":qs,'Aria':Aria,'building':building})

@login_required
def add_house_image(request):
  properts= House.objects.all()
  if request.method == 'POST':
    data =request.POST
    images =request.FILES.getlist('image')
    if data['propert'] != None:
      proper = House.objects.get(title=data['propert'])
      for img in images:
        galary.objects.create(
            proper=proper,
            image=img
        )
      return redirect('properts')

  return render(request, 'home/add_images.html', {'properts': properts})

@login_required
def add_property(request):
  proper = House.objects.all()
  form = house_form()
  if request.method == 'POST':
    form = house_form(request.POST or None, request.FILES or None)
    if form.is_valid():
      form.save()
      return redirect('add_images')

  return render(request, 'home/add_property.html',{'propertes':proper,'form':form})

@login_required
def update_property(request,slug):
  proper = get_object_or_404(House,slug=slug)
  if proper.Agent == request.user:
    form = house_form(request.POST or None,
                      request.FILES or None, instance=proper)
  else:
    return redirect('homepage')
  if request.method == 'POST':
    if form.is_valid():
      form.save()
  return render(request, 'home/update_property.html',{'form':form})

@login_required
def delete_property(request,slug):
  proper = get_object_or_404(House,slug=slug)
  if proper.Agent == request.user:
    proper.delete()
  return redirect('properts')


@login_required
def admin_propertes(request):
  proper =House.objects.all()
  p = Paginator(proper, 6)
  page_number = request.GET.get('page', 1)
  try:
      page_obj = p.get_page(page_number)
  except PageNotAnInteger:
      page_obj = p.page(1)
  except EmptyPage:
      page_obj = p.page(p.page_number)
  return render(request, 'home/property.html', {'page_obj': page_obj})

def searsh_property(request):
  searsh_product = request.GET['product']
  proper = House.objects.filter(title__icontains=searsh_product)
  p = Paginator(proper, 6)
  page_number = request.GET.get('page', 1)
  try:
      page_obj = p.get_page(page_number)
  except PageNotAnInteger:
      page_obj = p.page(1)
  except EmptyPage:
      page_obj = p.page(p.page_number)
  return render(request, 'home/searsh.html', {'page_obj': page_obj, 'count': proper.count(), })


@login_required
def add_house_info(request ,slug):
  proper =get_object_or_404(House,slug=slug)
  extra = extras.objects.filter(proper=proper)
  form = extra_form()
  if request.method == 'POST':
    form = extra_form(request.POST or None)
    if form.is_valid():
      form.save()

  return render(request, 'home/add_house_info.html', {'form': form, 'extras': extra, 'pro': proper})


def admin_settigns(request):
   form = UserUpdateForm(
       initial={
           'email': request.user.email,
           'username': request.user.username,
           'first_name': request.user.first_name or '',
           'last_name': request.user.last_name or '',
           'phone_number': request.user.phone_number or '',
       }
   )
   if request.method == 'POST':
      form = UserUpdateForm(
          request.POST or None,
          request.FILES or None, instance=request.user
      )
      if form.is_valid():
         form.save()
         return redirect('profile')
   return render(request, 'home/settings.html', {'form': form})


@login_required
def add_blog(request):
  form = blog_form()
  if request.method == 'POST':
    form = blog_form(request.POST or None, request.FILES or None)
    if form.is_valid():
      obj=form.save(commit=False)
      obj.auther = request.user
      obj.save()
      return redirect('blog_manager')

  return render(request, 'home/add_blog.html', {'form': form})


@login_required
def all_blog(request):
  blogs = blog.objects.all()
  p = Paginator(blogs, 6)
  page_number = request.GET.get('page', 1)
  try:
      page_obj = p.get_page(page_number)
  except PageNotAnInteger:
      page_obj = p.page(1)
  except EmptyPage:
      page_obj = p.page(p.page_number)
  return render(request, 'home/blog_manage.html', {'page_obj': page_obj})


@login_required
def update_blog(request, slug):
  blogs = get_object_or_404(blog, slug=slug)
  if blogs.auther == request.user:
    form = blog_form(request.POST or None,
                     request.FILES or None, instance=blogs)
  else:
    return redirect('homepage')
  if request.method == 'POST':
    if form.is_valid():
      form.save()
  return render(request, 'home/update_blog.html', {'form': form})


@login_required
def delete_blog(request, slug):
  blogs = get_object_or_404(blog, slug=slug)
  if blogs.auther == request.user:
    blogs.delete()
  return redirect('blog_manager')


@login_required
def dashbord(request):
  properts =House.objects.all().count()
  for_sell = House.objects.filter( property_type='للبيع').count()
  for_rent = House.objects.filter(status=True, property_type='للأيجار').count()
  under = House.objects.filter(status=False, property_type='للأيجار')
  agents =Acount.objects.all()
  return render(request,'home/dashboard.html',{'properts':properts,'for_sell':for_sell,'for_rent':for_rent,'agents':agents,'under':under})
