from checker import Checker

from .unit_check_content import kpi_format_unit_check
from .unit_check_headers import headersUnitCheck
from .unit_check_summary import (
    summary_report_name_unit_check,
    summary_report_period_present_unit_check,
    summary_report_period_format_unit_check,
    summary_report_period_interval_unit_check,
)


sample_report_checker = Checker(
    [
        summary_report_name_unit_check,
        summary_report_period_present_unit_check,
        summary_report_period_format_unit_check,
        summary_report_period_interval_unit_check,
        headersUnitCheck,
        kpi_format_unit_check,
    ]
)

__all__ = [
    sample_report_checker
]
