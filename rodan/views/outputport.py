import django_filters
from rest_framework import generics
from rest_framework import permissions
from rodan.models.outputport import OutputPort
from rodan.serializers.outputport import OutputPortSerializer
from rodan.paginators.pagination import PaginationSerializer


class OutputPortList(generics.ListCreateAPIView):
    """
    Returns a list of OutputPorts. Accepts a POST request with a data body to create
    a new OutputPort. POST requests will return the newly-created OutputPort object.
    """
    model = OutputPort
    serializer_class = OutputPortSerializer
    pagination_serializer_class = PaginationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = OutputPort.objects.all() # [TODO] restrict to the user's outputports?

    class filter_class(django_filters.FilterSet):
        workflow = django_filters.CharFilter(name='workflow_job__workflow')
        type = django_filters.CharFilter(name='output_port_type__name')
        class Meta:
            model = OutputPort
            fields = (
                "extern",
                "output_port_type",
                "workflow_job",
                "uuid",
                "label"
            )


class OutputPortDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Perform operations on a single OutputPort instance.
    """
    model = OutputPort
    serializer_class = OutputPortSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = OutputPort.objects.all() # [TODO] restrict to the user's outputports?
