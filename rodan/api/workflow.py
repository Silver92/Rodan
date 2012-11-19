from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields

from rodan.api.project import ProjectResource
from rodan.api.job import JobResource
from rodan.models.workflow import Workflow


class WorkflowResource(ModelResource):
    project = fields.ForeignKey(ProjectResource, 'project')
    jobs = fields.ManyToManyField(JobResource, 'jobs')

    class Meta:
        queryset = Workflow.objects.all()
        resource_name = "workflow"
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
