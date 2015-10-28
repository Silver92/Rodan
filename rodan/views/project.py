from rest_framework import generics
from rest_framework import permissions
from guardian.shortcuts import get_objects_for_user
from rodan.models.project import Project
from rodan.serializers.project import ProjectListSerializer, ProjectDetailSerializer
from rodan.serializers.user import UserSerializer


class ProjectList(generics.ListCreateAPIView):
    """
    Returns a list of Projects that the user has permissions to view. Accepts a POST
    request with a data body to create a new Project. POST requests will return the
    newly-created Project object.
    """
    model = Project
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProjectListSerializer
    queryset = Project.objects.all() # [TODO] restrict to the user's projects?
    filter_fields = {
        "updated": ['lt', 'gt'],
        "uuid": ['exact'],
        "created": ['lt', 'gt'],
        "creator": ['exact'],
        "name": ['exact', 'icontains'],
        "description": ['exact', 'icontains']
    }

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Performs operations on a single Project instance.
    """
    model = Project
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProjectDetailSerializer
    queryset = Project.objects.all() # [TODO] restrict to the user's projects?
