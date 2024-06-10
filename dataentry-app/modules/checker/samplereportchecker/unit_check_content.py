from ..checker import UnitCheck

import polars as pl
from polars import col


def check_kpi_format(file_path: str) -> bool:

    num_regex = r"(^[0-9]*$)|(^\.[0-9]*$)|(^[0-9]*\.[0-9]*$)"

    invalid_count = (
        pl
            .read_csv(file_path,has_header=True,skip_rows=3,infer_schema_length=0)
            .select(col("kpi").str.contains(num_regex).alias("validity"))
            .filter(col("validity") == False)
            .count()
            .item(0,0)
    )

    return (invalid_count == 0)

kpi_format_unit_check = UnitCheck(
    desc="""numeric values of 'kpi' column should be separated by `.` and not by `,`""",
    func=check_kpi_format
)
