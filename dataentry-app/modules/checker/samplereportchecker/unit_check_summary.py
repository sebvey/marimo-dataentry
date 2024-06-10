from checker.unitcheck import UnitCheck

import linecache
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def check_summary_report_name(file_path: str) -> bool:
    report_name_line = linecache.getline(file_path,1).strip()
    return (report_name_line == "report_name: to_test_report")

summary_report_name_unit_check = UnitCheck(
    desc="Report name should be given at line one with value 'report_name: to_test_report'",
    func=check_summary_report_name
)



def check_summary_report_period_present(file_path: str) -> bool:
    report_period_line = linecache.getline(file_path,2).strip()
    return report_period_line.startswith("period:")

summary_report_period_present_unit_check = UnitCheck(
    desc="Report period should be given at line two with value 'period: <Period Range>'",
    func=check_summary_report_period_present
)



def check_summary_report_period_format(file_path: str) -> bool:

    try:
        report_period_str = linecache.getline(file_path,2).strip()[8:]

        from_date = datetime.strptime(report_period_str[:8], '%d.%m.%y')
        to_date = datetime.strptime(report_period_str[11:], '%d.%m.%y')
        return True
    except ValueError:
        return False

summary_report_period_format_unit_check = UnitCheck(
    desc="Period Range should be formatted as 'DD.MM.YY - DD.MM.YY'",
    func=check_summary_report_period_format
)



def check_summary_report_period_interval(file_path: str) -> bool:

    try:
        report_period_str = linecache.getline(file_path,2).strip()[8:]
        from_dt = datetime.strptime(report_period_str[:8], '%d.%m.%y')
        to_dt = datetime.strptime(report_period_str[11:], '%d.%m.%y')

        return (
            (from_dt.day == 1) and
            ((to_dt + timedelta(days=1) - relativedelta(months=1)) == from_dt)
        )

    except ValueError:
        return False

summary_report_period_interval_unit_check = UnitCheck(
    desc="Period Range should covers one full month",
    func = check_summary_report_period_interval
)
