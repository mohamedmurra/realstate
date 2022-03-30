from rest_framework import serializers
from Main.models import House
from Blog.models import blog


class Housing_serlizer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'


class blog_serlizer(serializers.ModelSerializer):
    class Meta:
        model = blog
        fields = '__all__'
