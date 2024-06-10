from typing import ParamSpec, Callable
from dataclasses import dataclass
from xfp import Xeffect, XFXBranch

@dataclass
class StepError:
    step_name: str
    error: Exception

P = ParamSpec('P')

def failable_step[U](func: Callable[P,U]) -> Callable[P,Xeffect[StepError,U]]:

    def decorator(*args: P.args,**kwargs: P.kwargs):

        try:
            return Xeffect(
                branch=XFXBranch.RIGHT,
                value=func(*args,**kwargs),
                bias=XFXBranch.RIGHT
            )
        except Exception as e:
            return Xeffect(
                branch=XFXBranch.LEFT,
                value=StepError(step_name=func.__name__,error=e),
                bias=XFXBranch.RIGHT
            )

    return decorator

__all__ = [
    failable_step,
    StepError
]
