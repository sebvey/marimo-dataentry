from typing import Callable, Self, Optional

from dataclasses import dataclass


def bool_to_icon(b: Optional[bool]) -> str:
    if b is True:
        return '🟢'
    elif b is False:
        return '🔴'
    else:
        return '⚪'


@dataclass
class UnitCheckResult:
    desc: str
    is_successful: bool

    def __str__(self: Self) -> str:
        bold_tag = "" if self.is_successful  is None else "**"
        return bold_tag \
               + bool_to_icon(self.is_successful) \
               + " <- " + self.desc + bold_tag \
               + "  "


@dataclass
class UnitCheck:
    desc: str
    func: Callable[[str],bool]

    def run_on(self: Self, file_path: str) -> UnitCheckResult:
        return UnitCheckResult(self.desc,self.func(file_path))

    def ignore(self) -> UnitCheckResult:
        return UnitCheckResult(self.desc,None)
