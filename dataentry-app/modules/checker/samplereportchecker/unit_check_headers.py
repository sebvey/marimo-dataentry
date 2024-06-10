from checker.unitcheck import UnitCheck

import linecache

HEADERS_VALUE = '"id","kpi"'

def check_headers(file_path: str) -> bool:
    report_name_line = linecache.getline(file_path,4).strip()
    return (report_name_line == HEADERS_VALUE)

headersUnitCheck = UnitCheck(
    desc=f"""Headers should be at line four with value '{HEADERS_VALUE}'""",
    func=check_headers
)
