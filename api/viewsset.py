from rest_framework import viewsets, mixins, status, permissions
from rest_framework.response import Response
from Acounnt.models import Acount
from Main.models import Conatct, galary, extras
from api.serializers import Contact_Serializer, account_Serializer, admin_serializer, galary_Serializer, profile_serializer, team_serializer, extras_serializer
from .permissions import IsStaff


class admin_images_viewsets(viewsets.GenericViewSet, mixins.DestroyModelMixin):
    serializer_class = galary_Serializer
    queryset = galary.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        if user.is_staff or user == instance.proper.Agent:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'Not Authorized'}, status.HTTP_401_UNAUTHORIZED)


class admin_info_viewsets(viewsets.GenericViewSet, mixins.DestroyModelMixin):
    serializer_class = extras_serializer
    queryset = extras.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        if user.is_staff or user == instance.proper.Agent:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'Not Authorized'}, status.HTTP_401_UNAUTHORIZED)



class Profile_viewset(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    serializer_class = profile_serializer
    queryset = Acount.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = self.request.user
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if user.is_admin:
            serializer = admin_serializer(
                instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        elif user.is_staff:
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        elif user.id == instance.id:
            serializer = team_serializer(
                instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response({'Not Authorized'}, status.HTTP_401_UNAUTHORIZED)


class Messages(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    serializer_class = Contact_Serializer
    queryset = Conatct.objects.filter(status=False)
    lookup_field = 'id'
    permission_classes = [IsStaff]


class users(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    serializer_class = profile_serializer
    queryset = Acount.objects.all().exclude(is_staff=True)
    lookup_field = 'id'
    permission_classes = [IsStaff]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_admin:
            queryset = Acount.objects.all().exclude(is_admin=True)
        else:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            if user.is_admin:
                serializer = admin_serializer(page, many=True)
            else:
                serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        if user.is_admin:
            serializer = admin_serializer(queryset, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
