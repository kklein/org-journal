import logging
import shutil
from pathlib import Path

import click

_TEMPLATE_WEEK = "template_week.org"
_TEMPLATE_MONTH_BEFORE = "template_month_before.org"
_TEMPLATE_MONTH_AFTER = "template_month_after.org"

_WEEKS = "weeks"
_MONTHS = "months"

_N_WEEKS = 52
_N_MONTHS = 12

_ORG_FILE_ENDING = ".org"


def _month_name(month_number: int) -> str:
    names = [
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
    ]
    return names[month_number - 1]


def month_filename(month_number: int, use_before: bool) -> str:
    return (
        str(month_number)
        + "-"
        + _month_name(month_number)
        + "_"
        + ("pre" if use_before else "post")
        + _ORG_FILE_ENDING
    )


def copy_file(origin: Path, destination: Path):
    if destination.exists() and destination.is_file():
        logging.info(f"Skipping file {destination} since it already exists.")
    else:
        shutil.copy2(origin, destination)


def setup_weeks(root_dir: Path):
    weeks_dir = root_dir / _WEEKS
    weeks_dir.mkdir(exist_ok=True)
    for week_number in range(1, _N_WEEKS + 1):
        filepath = weeks_dir / (str(week_number) + _ORG_FILE_ENDING)
        copy_file(Path(_TEMPLATE_WEEK), filepath)
    logging.info("Finished setting up week files.")


def setup_months(root_dir: Path):
    months_dir = root_dir / _MONTHS
    months_dir.mkdir(exist_ok=True)
    for month_number in range(1, _N_MONTHS + 1):
        filepath_before = months_dir / month_filename(month_number, use_before=True)
        copy_file(Path(_TEMPLATE_MONTH_BEFORE), filepath_before)
        filepath_after = months_dir / month_filename(month_number, use_before=False)
        copy_file(Path(_TEMPLATE_MONTH_AFTER), filepath_after)
    logging.info("Finished setting up month files.")


@click.command()
@click.argument("root_dir", type=click.Path(exists=True))
def main_cli(root_dir):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    root_logger.addHandler(stream_handler)
    setup_weeks(Path(root_dir))
    setup_months(Path(root_dir))


if __name__ == "__main__":
    main_cli()
