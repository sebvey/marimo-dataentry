import marimo

__generated_with = "0.6.22"
app = marimo.App(width="medium", app_title="Data Entry")


@app.cell
def __():
    from typing import Optional

    import marimo as mo

    from dataclasses import asdict
    from pathlib import Path
    from xfp import Xeffect,XFXBranch

    from domain import UIFile
    from pipeline import Pipeline, PipeConf, PipeState
    from checker.samplereportchecker import sample_report_checker
    from uploader import AWSUploaderMock
    return (
        AWSUploaderMock,
        Optional,
        Path,
        PipeConf,
        PipeState,
        Pipeline,
        UIFile,
        XFXBranch,
        Xeffect,
        asdict,
        mo,
        sample_report_checker,
    )


@app.cell
def __(Html, UIFile, mo):
    def watch_and_get_marimo_file(file_uploader_ui: Html) -> UIFile:

        # The `mo.ui.file` object is defined, with `value` initially set to Tuple()
        # We stop execution until a file is actually loaded
        mo.stop(len(file_uploader_ui.value) == 0)

        return UIFile(
            file_uploader_ui.value[0].name,
            file_uploader_ui.value[0].contents
        )
    return watch_and_get_marimo_file,


@app.cell
def __(
    AWSUploaderMock,
    Path,
    PipeConf,
    PipeState,
    Pipeline,
    UIFile,
    sample_report_checker,
):
    def run_pipeline(ui_file: UIFile) -> PipeState:

        ### FOR TESTING PURPOSE
        # Whether a step of the pipeline should raise an Exception
        # Set to True -> the Mocked uploader will raise Exception("TEST EXCEPTION")
        PIPELINE_SHOULD_FAIL = False

        ## I only implement a Mock uploader, that fails or success on demand
        mocked_aws_uploader = AWSUploaderMock(
            bucket='my_destination_bucket',
            target_prefix='my/target/prefix',
            is_lame=PIPELINE_SHOULD_FAIL
        )

        pipe_conf = PipeConf(
            ui_file = ui_file,
            checker = sample_report_checker,
            uploader = mocked_aws_uploader,
            working_path=Path('tmp'),
        )

        # Pipeline is a context manager
        # The file is written on disk locally for the check
        # -> If a Exception is raised during the pipeline,
        #    the tmp resources on disk are deleted anyway

        with Pipeline(pipe_conf) as pipeline:
            pipe_result = pipeline.run()

            # 'result' is a Xeffect[StepError,PipeState]
            # Xeffect is a class from 'xfp' package that helps dealing with
            # unpure types (here tryable values) in a functinoal way
            # Xeffect is used in the Pipeline implementation catch exceptions
            # and wrap them as a StepError
            # -> See README.md for more details on xfp module

        return pipe_result
    return run_pipeline,


@app.cell
def __(Html, PipeState, StepError, XFXBranch, Xeffect, mo):
    UPLOADED_MSG = f"## {mo.icon("lucide:cloud-upload")} FILE UPLOADED TO THE DATA PLATFORM"
    NOT_UPLOADED_MSG = f"## {mo.icon("lucide:circle-arrow-right")} FILE NOT UPLOADED TO THE DATA PLATFORM"

    def get_failure_msg(se: StepError):
        return f"""## {mo.icon("lucide:siren")} PIPELINE FAILED - CALL THE DATA TEAM :
                   **Step Concerned    :** {se.step_name}
                   **Exception Type    :** {type(se.error)}
                   **Exception Message :** {se.error}
                """


    def get_final_callout(pipe_result: Xeffect[StepError, PipeState]) -> Html:

        def get_success_callout(pipe_state: PipeState) -> Html:

            check_callout_kind = 'success' if pipe_state.check_result.is_successful else 'warn'
            check_callout = mo.md(str(pipe_state.check_result)).callout(kind=check_callout_kind)

            upload_msg, upload_callout_kind = (
                (UPLOADED_MSG, 'success')
                if pipe_state.upload_done
                else (NOT_UPLOADED_MSG, 'warn')
            )

            upload_callout = mo.md(upload_msg).callout(kind=upload_callout_kind)

            return mo.vstack([check_callout,upload_callout])

        def get_failure_callout(step_error: StepError) -> Html:
            return mo.md(get_failure_msg(step_error)).callout(kind='danger')


        return (
            get_success_callout(pipe_result.value)
            if pipe_result.branch == XFXBranch.RIGHT
            else get_failure_callout(pipe_result.value)
        )
    return (
        NOT_UPLOADED_MSG,
        UPLOADED_MSG,
        get_failure_msg,
        get_final_callout,
    )


@app.cell
def __(mo):
    mo.md(f"# {mo.icon('lucide:file-text')} DATA ENTRY")
    return


@app.cell
def __(mo):
    file_uploader_ui = mo.ui.file(
        filetypes=[".csv"], kind="area", label="Upload a file"
    )
    file_uploader_ui
    return file_uploader_ui,


@app.cell
def __(file_uploader_ui, watch_and_get_marimo_file):
    ui_file = watch_and_get_marimo_file(file_uploader_ui)
    return ui_file,


@app.cell
def __(run_pipeline, ui_file):
    pipe_result = run_pipeline(ui_file)
    return pipe_result,


@app.cell
def __(get_final_callout, pipe_result):
    final_callout = get_final_callout(pipe_result)
    final_callout
    return final_callout,


if __name__ == "__main__":
    app.run()
