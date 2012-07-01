import json

import gamera.gamera_xml
import gamera.core

import utils
from aomr_resources.AomrObjectOrig import AomrObject
from aomr_resources.AomrMeiOutput import AomrMeiOutput
from rodan.models.jobs import JobType, JobBase

@utils.rodan_task(inputs=('xml'), others=['segmented_image', 'page_sequence'])
def pitch_find(xml_filepath, segmented,  page_sequence, **kwargs):
    # Run a rank filter on the image to make the staves bigger
    #  for pitch detection
    print "loading image... performing rank filter"
    input_image = utils.load_image_for_job(segmented, gamera.plugins.misc_filters.rank)
    # XXX: Parameters to change?
    rank_image = input_image.rank(9, 9, 0)

    #gamera.core.save_image(rank_image, "aomr2-rank.tiff")
    print "... done. Finding pitches"
    aomr_obj = AomrObject(rank_image, \
        discard_size=kwargs['discard_size'],
        lines_per_staff=4,
        staff_finder=0,
        staff_removal=0,
        binarization=0)
    glyphs = gamera.gamera_xml.glyphs_from_xml(xml_filepath)

    recognized_glyphs = aomr_obj.run(glyphs)
    print "... done. Writing MEI"
    data = json.loads(recognized_glyphs)
    mei_file = AomrMeiOutput(data, str(segmented), str(page_sequence))

    return {
        'mei': mei_file
    }


class PitchFindingFull(JobBase):
    """ Perform pitch finding by doing the staff recognition in the job, not outside """
    name = 'Pitch finding (image input)'
    slug = 'pitch-finding-full'
    input_type = JobType.CLASSIFY_XML
    output_type = JobType.MEI
    description = 'Generate an MEI file containing the notes on the page'
    show_during_wf_create = True
    parameters = {
        'discard_size': 12
    }
    task = pitch_find
    is_automatic = True
    outputs_image = False