from pathlib import Path

from domain import UIFile
from pipeline import Pipeline, PipeConf
from checker.samplereportchecker import sample_report_checker
from uploader import AWSUploaderMock


# From mo.ui.file() marimo component
# This binary file is valid (it will pass the check)
file_content = \
b"""report_name: to_test_report
period: 01.10.24 - 31.10.24

"id","kpi"
"1","1.0"
"2",".02"
"3","333"
"""

### FOR TESTING PURPOSE
# Whether a step of the pipeline should raise an Exception
# Set to True -> the Mocked uploader will raise Exception("TEST EXCEPTION")
PIPELINE_SHOULD_FAIL = True


### I only implement a Mock uploader, that fails or success on demand
aws_uploader = AWSUploaderMock(
        bucket='my_destination_bucket',
        target_prefix='my/target/prefix',
        is_lame = PIPELINE_SHOULD_FAIL
)

pipe_conf = PipeConf(
    ui_file = UIFile("my_file", file_content),
    checker = sample_report_checker,
    uploader = aws_uploader,
    working_path=Path('tmp'),
)


### Pipeline is a context manager
# The file is written on disk locally for the check
# -> If a Exception is raised during the pipeline,
#    the tmp resources on disk are deleted anyway
with Pipeline(pipe_conf) as pipeline:

    ### 'result' is a Xeffect[StepError,PipeState]
    # Xeffect is a class from 'xfp' package that helps dealing with
    # unpure types (here tryable values) in a functinoal way
    # Xeffect is used in the Pipeline implementation catch exceptions
    # and wrap them as a StepError
    # -> See README.md for more details on xfp module
    result = pipeline.run()

### Later in the interface, 
