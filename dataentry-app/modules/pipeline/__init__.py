from typing import Self, Optional
from dataclasses import dataclass, replace

from pathlib import Path
import uuid
from shutil import rmtree
from xfp import Xeffect, XFXBranch

from pipeline.step import failable_step, StepError
from checker import Checker, CheckResult
from domain import UIFile
from uploader import Uploader


@dataclass(frozen=True)
class PipeState:
    check_result: Optional[CheckResult] = None
    upload_done: Optional[bool] = None


@dataclass(frozen=True)
class PipeConf:
    ui_file: UIFile
    checker: Checker
    uploader: Uploader
    working_path: Path


class Pipeline:

    def __init__(self: Self, conf: PipeConf) -> None:
        self._conf: PipeConf = conf
        self._tmp_path: Path = conf.working_path / str(uuid.uuid4())
        self._local_file_path = self._tmp_path / conf.ui_file.name


    def __enter__(self: Self) -> 'Pipeline':

        self._tmp_path.mkdir(parents=True)

        with self._local_file_path.open(mode="wb") as f:
            f.write(self._conf.ui_file.contents)

        return self


    def __exit__(self: Self, exc_type, exc_value, exc_tb) -> bool:
        rmtree(self._tmp_path)


    ## PIPELINE STEPS

    @failable_step
    def _check_file(self: Self, state: PipeState) -> PipeState:

        check_result = self._conf.checker.run_on(self._local_file_path)
        return replace(state,check_result=check_result)


    @failable_step
    def _upload(self: Self, state: PipeState) -> PipeState:

        if state.check_result.is_successful:
            self._conf.uploader.upload(self._local_file_path)
            upload_done = True

        else:
            upload_done = False

        return replace(state,upload_done=upload_done)


    def run(self) -> Xeffect[StepError, PipeState]:

        return (
            Xeffect
                .lift(PipeState())
                .flat_map(self._check_file)
                .flat_map(self._upload)
        )


__all__ = [
    PipeState,
    PipeConf,
    Pipeline
]
