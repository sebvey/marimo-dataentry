from typing import List, Self

from dataclasses import dataclass
from pathlib import Path
import marimo as mo

from .unitcheck import UnitCheck, UnitCheckResult


@dataclass
class CheckResult:
    is_successful: bool
    unit_check_results: List[UnitCheckResult]

    def __str__(self: Self) -> str:

        if self.is_successful:
            str_header = f"## {mo.icon("lucide:grid-2x2-check")} CHECK SUCCEDED"
        else:
            str_header = f"## {mo.icon("lucide:grid-2x2-x")} CHECK FAILED"

        return "\n".join(
            [str_header] +
            [ str(ucr) for ucr in self.unit_check_results]
        )

@dataclass
class Checker:
    unit_checks: List[UnitCheck]


    def run_on(self,file_path: Path) -> CheckResult:

        previous_unit_checks_successful = True
        unit_check_results: List[UnitCheck] = []

        for unit_check in self.unit_checks:
            if previous_unit_checks_successful:
                    unit_check_result = unit_check.run_on(str(file_path))
                    unit_check_results.append(unit_check_result)
                    previous_unit_checks_successful = unit_check_result.is_successful
            else:
                unit_check_results.append(unit_check.ignore())

        return CheckResult(
            is_successful=previous_unit_checks_successful,
            unit_check_results=unit_check_results
        )
