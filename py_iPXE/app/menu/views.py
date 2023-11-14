from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import iPXE_Menu, Watched_File, Watched_Directory, Tracked_Directories
from .serializers import iPXE_Menu_Serializer, iPXE_Menu_item_Serializer, iPXE_File_Serializer
from django.db import transaction
from datetime import datetime
from pathlib import Path
from rest_framework.response import Response

class MenuViewSet(viewsets.ModelViewSet):
    queryset = iPXE_Menu.objects.all()
    serializer_class = iPXE_Menu_Serializer
        
    def perform_create(self, serializer):
        # Extract and create iPXE_Menu_item instances
        steps_data = self.request.data.get('steps', [])
        steps_instances = [iPXE_Menu_item_Serializer(data=step_data).save() for step_data in steps_data]

        # Set the created iPXE_Menu_item instances in the serializer
        serializer.validated_data['steps'] = steps_instances

        # Save the iPXE_Menu instance
        serializer.save()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title')
        if title is not None:
            queryset = queryset.filter(title=title)

        return queryset

class WimagerViewSet(viewsets.ModelViewSet):
    queryset = Watched_File.objects.all()
    serializer_class = iPXE_File_Serializer
    base_path = "/media/audientvoid/BKC_wim"

    @staticmethod
    @transaction.atomic
    def wims_from_dir(base_dir):
        wim_files = Watched_File.objects.all()
        base_path = Path(base_dir)

        for path in base_path.rglob("*.wim"):
            if path.is_file():
                file_name = path.name
                folder = str(path.parent)
                timestamp = datetime.utcfromtimestamp(path.stat().st_mtime)

                file_obj, created = wim_files.get_or_create(
                    file_name=file_name,
                    defaults={'file_path': folder, 'last_edited': timestamp}
                )

                if not created:
                    file_obj.file_path = folder
                    file_obj.last_edited = timestamp
                    file_obj.save()

                dir_obj, created = Watched_Directory.objects.get_or_create(
                    absolute_path=folder
                )

                if not created:
                    dir_obj.files.add(file_obj)

                tracked_dir_obj, created = Tracked_Directories.objects.get_or_create(id=1)

                if not created:
                    tracked_dir_obj.directory.add(dir_obj)

                tracked_dir_obj.last_updated = datetime.now()
                tracked_dir_obj.save()


    def perform_scan(self):
        return self.wims_from_dir(base_dir=self.base_path)

    def list(self, request, *args, **kwargs):
        # Trigger perform_scan before returning the list of objects
        self.perform_scan()

        # Continue with the default list behavior
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
