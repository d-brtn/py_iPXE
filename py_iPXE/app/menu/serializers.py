#serializers.py
from django.contrib.auth.models import User,Group
from rest_framework import serializers
from .models import iPXE_Menu, iPXE_Menu_item, Watched_File

class iPXE_Menu_item_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = iPXE_Menu_item
        fields = ['item_name','item_contents']

class iPXE_Menu_Serializer(serializers.HyperlinkedModelSerializer):
    steps = iPXE_Menu_item_Serializer(many=True)
    class Meta:
        model = iPXE_Menu
        fields = ['title','steps']
        depth = 3

    def create(self, validated_data):
        steps_data = validated_data.pop('steps', [])
        menu_instance = iPXE_Menu.objects.create(**validated_data)
        menu_instance.steps.set(steps_data)  # Set the many-to-many relationship
        return menu_instance
    
class iPXE_File_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Watched_File
        fields = ['file_name','file_path','last_edited']