
from Main.models import aria, Comment, extras, Building, Purpose, House, galary, Testomany, Conatct, Rent
from rest_framework import serializers
from Blog.models import Catagoryes, blog
from Acounnt.models import Acount
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer


user = get_user_model()


class galary_Serializer(serializers.ModelSerializer):
    class Meta:
        model = galary
        fields = '__all__'


class Rent_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = '__all__'


class Contact_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Conatct
        fields = '__all__'


class profile_serializer(serializers.ModelSerializer):
    class Meta:
        model = Acount
        fields = ('image', 'phone_number', 'username', 'email', 'id', 'date_joined',
                  'first_name', 'last_name', 'gender', 'describe', 'whatssap', 'user_type', 'is_active')


class admin_serializer(serializers.ModelSerializer):
    class Meta:
        model = Acount
        fields = ('image', 'phone_number', 'username', 'email', 'id', 'date_joined',
                  'first_name', 'last_name', 'gender', 'describe', 'whatssap', 'user_type', 'is_active', 'is_staff')


class Purpose_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Purpose
        fields = '__all__'


class extras_serializer(serializers.ModelSerializer):
    class Meta:
        model = extras
        fields = '__all__'


class aria_serializer(serializers.ModelSerializer):
    class Meta:
        model = aria
        fields = '__all__'


class buillding_serializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'


class account_Serializer(UserCreateSerializer):
    class Meta:
        model = Acount
        fields = ('image', 'phone_number', 'username', 'email', 'id', 'date_joined',
                  'first_name', 'last_name', 'gender', 'describe', 'whatssap', 'user_type')


class add_house(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'


class Seasrh_serializer(serializers.Serializer):
    buildings = serializers.SerializerMethodField()
    lucation = serializers.SerializerMethodField()
    purp = serializers.SerializerMethodField()
    rent_time = serializers.SerializerMethodField()

    def get_buildings(self, obj):
        house = Building.objects.all()
        data = buillding_serializer(house, many=True).data
        return data

    def get_lucation(self, obj):
        ara = aria.objects.all()
        data = aria_serializer(ara, many=True).data
        return data

    def get_purp(self, obj):
        pur = Purpose.objects.all()
        data = Purpose_Serializer(pur, many=True).data
        return data

    def get_rent_time(self, obj):
        ob = Rent.objects.all()
        data = Purpose_Serializer(ob, many=True).data
        return data


class team_serializer(serializers.ModelSerializer):
    class Meta:
        model = Acount
        fields = ('id', 'username', 'email', 'phone_number',
                  'image', 'describe', 'first_name', 'last_name', 'whatssap', 'date_joined')


class update_house_serializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'


class Housing_serlizer(serializers.ModelSerializer):
    aria = serializers.StringRelatedField()
    property_type = serializers.StringRelatedField()
    building_type = serializers.StringRelatedField()
    rent_type = serializers.StringRelatedField()
    Agent = team_serializer()
    images = serializers.SerializerMethodField()

    class Meta:
        model = House
        fields = '__all__'

    def get_images(self, obj):
        house = galary.objects.filter(proper_id=obj.id)
        data = galary_Serializer(house, many=True).data
        return data


class admin_Housing_serlizer(serializers.ModelSerializer):
    aria = aria_serializer()
    property_type = Purpose_Serializer()
    building_type = buillding_serializer()
    rent_type = Rent_Serializer()
    Agent = team_serializer()

    class Meta:
        model = House
        fields = '__all__'


class Comment_serializer(serializers.ModelSerializer):
    user = team_serializer()

    class Meta:
        model = Comment
        fields = '__all__'


class Add_Comment_serializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class house_detail_serializer(serializers.ModelSerializer):
    rent_type = serializers.StringRelatedField()
    images = serializers.SerializerMethodField()
    Related = serializers.SerializerMethodField()
    info = serializers.SerializerMethodField()
    aria = serializers.StringRelatedField()
    Agent = team_serializer()
    property_type = serializers.StringRelatedField()
    building_type = serializers.StringRelatedField()
    comment = serializers.SerializerMethodField()

    class Meta:
        model = House
        fields = '__all__'

    def get_images(self, obj):
        house = galary.objects.filter(proper_id=obj.id)
        data = galary_Serializer(house, many=True).data
        return data

    def get_info(self, obj):
        info = extras.objects.filter(proper_id=obj.id)
        data = extras_serializer(info, many=True).data
        return data

    def get_Related(sekf, obj):
        houses = House.objects.filter(aria=obj.aria).exclude(id=obj.id)
        data = Housing_serlizer(houses, many=True).data
        return data

    def get_comment(self, obj):
        comment = Comment.objects.filter(proper_id=obj.id).order_by('-created')
        data = Comment_serializer(comment, many=True).data
        return data


class blog_cata_serlizer(serializers.ModelSerializer):
    class Meta:
        model = Catagoryes
        fields = '__all__'


class blog_serlizer(serializers.ModelSerializer):
    catagory = serializers.StringRelatedField()
    auther = team_serializer()

    class Meta:
        model = blog
        fields = '__all__'


class Testemany_serializer(serializers.ModelSerializer):
    class Meta:
        model = Testomany
        fields = '__all__'


class galary_serializer(serializers.ModelSerializer):
    class Meta:
        model = galary
        fields = '__all__'


class agent_serializer(serializers.ModelSerializer):
    proper = serializers.SerializerMethodField()

    class Meta:
        model = Acount
        fields = ('id', 'username', 'email', 'phone_number',
                  'image', 'describe', 'first_name', 'last_name', 'proper', 'whatssap', 'user_type')

    def get_proper(self, obj):
        pro = House.objects.filter(Agent=obj.id)
        data = Housing_serlizer(pro, many=True).data
        return data


class homepage_serializer(serializers.Serializer):
    latest_property = serializers.SerializerMethodField()
    latest_blog = serializers.SerializerMethodField()
    Testomany = serializers.SerializerMethodField()
    Team = serializers.SerializerMethodField()
    tess = serializers.SerializerMethodField()

    def get_latest_property(self, obj):
        house = House.objects.all().order_by('-created')[:5]
        data = Housing_serlizer(house, many=True).data
        return data

    def get_latest_blog(self, obj):
        blogs = blog.objects.all().order_by('-created')[:5]
        data = blog_serlizer(blogs, many=True).data
        return data

    def get_tess(self, obj):
        teste = Testomany.objects.all()
        data = Testemany_serializer(teste, many=True).data
        return data

    def get_Testomany(self, obj):
        teste = Testomany.objects.all().order_by('-created')[:5]
        data = Testemany_serializer(teste, many=True).data
        return data

    def get_Team(self, obj):
        teste = Acount.objects.filter(is_staff=True)
        data = team_serializer(teste, many=True).data
        return data


class add_blog_serlizer(serializers.ModelSerializer):
    class Meta:
        model = blog
        fields = '__all__'


class admin_dashbord(serializers.Serializer):
    rooms = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()

    def get_rooms(self, obj):
        house = House.objects.all().order_by('-created')
        data = Housing_serlizer(house, many=True).data
        return data

    def get_users(self, obj):
        users = Acount.objects.filter(
            is_staff=False).order_by('-date_joined')
        data = team_serializer(users, many=True).data
        return data


class adminblog_serlizer(serializers.ModelSerializer):
    catagory = blog_cata_serlizer()
    auther = team_serializer()

    class Meta:
        model = blog
        fields = '__all__'
