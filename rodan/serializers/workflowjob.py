from rodan.models.workflowjob import WorkflowJob
from rest_framework import serializers


class WorkflowJobSerializer(serializers.HyperlinkedModelSerializer):
    workflow = serializers.HyperlinkedRelatedField(view_name="workflow-detail")
    job = serializers.HyperlinkedRelatedField(view_name="job-detail")
    sequence = serializers.IntegerField(required=False)
    job_settings = serializers.CharField(required=False)  # this actually sends it as a JSON object
    needs_input = serializers.BooleanField(required=False)
    job_type = serializers.IntegerField(required=False)

    job_name = serializers.Field(source="job_name")
    job_description = serializers.Field(source="job_description")
    input_pixel_types = serializers.Field(source="input_pixel_types")
    output_pixel_types = serializers.Field(source="output_pixel_types")

    class Meta:
        model = WorkflowJob
        read_only_fields = ('created', 'updated')
        fields = ("url",
                  "workflow",
                  "input_pixel_types",
                  "output_pixel_types",
                  "job_name",
                  "job_description",
                  "job_type",
                  "job",
                  "workflow_run",
                  "needs_input",
                  "sequence",
                  "job_settings",
                  "created",
                  "updated")
