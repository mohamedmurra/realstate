
from rest_framework.parsers import FormParser, MultiPartParser
from Acounnt.models import Acount
from rest_framework.authtoken.models import Token
from requests.exceptions import HTTPError
from rest_framework import filters
from django.shortcuts import get_object_or_404, render
from .serializers import Housing_serlizer, account_Serializer, admin_Housing_serlizer, admin_dashbord, blog_serlizer, galary_Serializer, house_detail_serializer, Testemany_serializer, Purpose_Serializer, aria_serializer, extras_serializer, team_serializer, agent_serializer, Comment_serializer, homepage_serializer, Seasrh_serializer, Contact_Serializer, profile_serializer, Add_Comment_serializer, add_house, blog_cata_serlizer, add_blog_serlizer, update_house_serializer, adminblog_serlizer, buillding_serializer
from rest_framework import generics, status, pagination, permissions, authentication, viewsets
from Main.models import Conatct,  House, aria, galary, Testomany, Purpose, extras, Comment
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from Blog.models import blog, Catagoryes
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsStaff
from social_django.utils import psa

# Create your views here.


class MyPagination(pagination.PageNumberPagination):
    page_size = 6

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })


@api_view(['GET', ])
def admin_view(request):
    add = get_object_or_404(Acount, is_admin=True)
    seria = profile_serializer(add)
    return Response(seria.data)


@api_view(['GET', ])
def get_images_view(request, id):
    pro = galary.objects.filter(proper__id=id)
    seria = galary_Serializer(pro, many=True)
    return Response(seria.data)


class ContactView(generics.CreateAPIView):
    serializer_class = Contact_Serializer
    queryset = Conatct.objects.all()


class Add_coment_view(generics.CreateAPIView):
    serializer_class = Add_Comment_serializer
    queryset = Comment.objects.all()


class house_view(generics.ListCreateAPIView):
    serializer_class = Housing_serlizer
    queryset = House.objects.filter(status=True).order_by('-created')
    pagination_class = MyPagination
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['building_type', 'num_rooms',
                        'status', 'property_type', 'aria', 'bathrooms']
    search_fields = ['title', 'num_rooms', 'bathrooms', ]
    ordering_fields = ['price', 'num_rooms', 'bathrooms', 'created']

    def get_queryset(self):
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if max_price and not min_price:
            return House.objects.filter(price__lte=max_price)
        if min_price and not max_price:
            return House.objects.filter(price__gte=min_price)
        if min_price and max_price:
            return House.objects.filter(price__lte=max_price, price__gte=min_price)
        return super().get_queryset()


class house_view_all(generics.ListAPIView):
    serializer_class = Housing_serlizer
    queryset = House.objects.all()


class admin_house_images(generics.ListAPIView):
    serializer_class = Housing_serlizer
    queryset = House.objects.all().order_by('-created')
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return House.objects.filter(Agent__id=user.id)


class admin_house_view(generics.ListAPIView):
    serializer_class = admin_Housing_serlizer
    queryset = House.objects.all().order_by('-created')

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return House.objects.all()
        else:
            return House.objects.filter(Agent__id=user.id)


class admin_blog_view(generics.ListAPIView):
    serializer_class = adminblog_serlizer
    queryset = blog.objects.all().order_by('-created')
    pagination_class = MyPagination


class add_house_view(generics.CreateAPIView):
    serializer_class = add_house
    queryset = House.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class favourties_view(generics.ListAPIView):
    serializer_class = Housing_serlizer
    queryset = House.objects.all().order_by('-created')
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MyPagination

    def get_queryset(self):
        user = self.request.user
        obj = user.favourties.all()
        return obj


class favo_add(APIView):
    def post(self, request):
        house = get_object_or_404(House, slug=request.data.get('slug'))
        if request.user not in house.favourties.all():
            house.favourties.add(request.user)
            return Response({'detail': 'Property been added to your fav'}, status=status.HTTP_200_OK)
        return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)


class favo_remove(APIView):
    def post(self, request):
        house = get_object_or_404(House, slug=request.data.get('slug'))
        if request.user in house.favourties.all():
            house.favourties.remove(request.user)
            return Response({'detail': 'Property been removed from your fav'}, status=status.HTTP_200_OK)
        return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def Searsh_filter(request):
    admin = Acount.objects.get(is_admin=True)
    seria = Seasrh_serializer(admin)
    return Response(seria.data)


@api_view(['GET', ])
def homepage_view(request):
    admin = Acount.objects.get(is_admin=True)
    seria = homepage_serializer(admin)
    return Response(seria.data)


class galary_view(generics.CreateAPIView):
    serializer_class = galary_Serializer
    queryset = galary.objects.all()
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        images = data.getlist('image')
        proper = data.get('proper')

        if not images:
            return super().create(request, *args, **kwargs)

        serializer_lst = []
        for image in images:
            data['image'] = image
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer_lst.append(serializer)
        serializer_data = []
        for serializer in serializer_lst:
            self.perform_create(serializer)
            serializer_data.append(serializer.data)
            headers = self.get_success_headers(serializer.data)
        return Response(serializer_data, status=status.HTTP_201_CREATED, headers=headers)


class Purpose_view(generics.ListCreateAPIView):
    serializer_class = Purpose_Serializer
    queryset = Purpose.objects.all()


class aria_view(generics.ListCreateAPIView):
    serializer_class = aria_serializer
    queryset = aria.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_staff:
            return self.create(request, *args, **kwargs)
        else:
            return Response('Not Authorize', status.HTTP_401_UNAUTHORIZED)


class add_building(generics.CreateAPIView):
    serializer_class = buillding_serializer
    queryset = aria.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_staff:
            return self.create(request, *args, **kwargs)
        else:
            return Response('Not Authorize', status.HTTP_401_UNAUTHORIZED)


class add_info_view(generics.ListCreateAPIView):
    serializer_class = extras_serializer
    queryset = extras.objects.all()

    def post(self, request, *args, **kwargs):
        user = self.request.user
        proper = request.data['proper']
        porpert = get_object_or_404(House, id=proper)
        if porpert.Agent == user:
            return self.create(request, *args, **kwargs)
        else:
            return Response('Not Authorize', status.HTTP_401_UNAUTHORIZED)


class Testemonay_view(generics.CreateAPIView):
    serializer_class = Testemany_serializer
    queryset = Testomany.objects.all()


@api_view(['GET', ])
def Dashbord_view(request):
    add = get_object_or_404(Acount, is_admin=True)
    seria = admin_dashbord(add)
    return Response(seria.data)


class get_house(generics.RetrieveAPIView):
    serializer_class = house_detail_serializer
    queryset = House.objects.all()
    lookup_field = 'slug'


class update_house(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = update_house_serializer
    queryset = House.objects.all()
    lookup_field = 'slug'


class update_blog(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = adminblog_serlizer
    queryset = blog.objects.all()
    lookup_field = 'slug'


class user_detail(generics.RetrieveUpdateAPIView):
    serializer_class = profile_serializer
    queryset = Acount.objects.all()
    lookup_field = 'id'


class blog_view(generics.ListAPIView):
    serializer_class = blog_serlizer
    queryset = blog.objects.all().order_by('-created')
    pagination_class = MyPagination


class blog_catagory_view(generics.ListCreateAPIView):
    serializer_class = blog_cata_serlizer
    queryset = Catagoryes.objects.all()
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class add_blog_view(generics.CreateAPIView):
    serializer_class = add_blog_serlizer
    queryset = blog.objects.all()
    # permission_classes = [permissions.IsAuthenticated]


class get_blog(generics.RetrieveAPIView):
    serializer_class = blog_serlizer
    queryset = blog.objects.all()
    lookup_field = 'slug'


class Teammember(generics.ListAPIView):
    serializer_class = team_serializer
    queryset = Acount.objects.filter(is_staff=True)
    pagination_class = MyPagination


class users(generics.ListAPIView):
    serializer_class = profile_serializer
    queryset = Acount.objects.all().exclude(is_admin=True)


class users_update(generics.RetrieveUpdateAPIView):
    serializer_class = profile_serializer
    queryset = Acount.objects.all()
    lookup_field = 'id'


class Agent_detail(generics.RetrieveAPIView):
    serializer_class = agent_serializer
    queryset = Acount.objects.all()
    lookup_field = 'id'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        if user.image:
            token['image'] = user.image.url
        token['username'] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class BlackListTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@psa()
def Register_by_Acsses_token(request, backend):
    token = request.data.get('access_token')
    user = request.backend.do_auth(token)
    print(request)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(refresh),
                'token': str(refresh.access_token)
            },
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {
                'errors': {
                    'token': 'Invalid token'
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )
