"""
Create and initialize a new pipeline directory
"""
import logging
from pathlib import Path
from importlib.resources import files

from . import CommandLineError


logger = logging.getLogger(__name__)


def add_arguments(parser):
    parser.add_argument("directory", type=Path, help="New pipeline directory to create")


def main(args, arguments):
    if arguments:
        raise CommandLineError("These arguments are unknown: %s", arguments)
    run_init(**vars(args))


def run_init(directory: Path):
    if " " in str(directory):
        raise CommandLineError(
            "The name of the pipeline directory must not contain spaces"
        )

    try:
        directory.mkdir(exist_ok=True)
    except OSError as e:
        raise CommandLineError(e)

    configuration = files("ductape").joinpath("ductape.yaml").read_text()
    with open(Path(directory) / "ductape.yaml", "w") as f:
        f.write(configuration)

    samplesheet = files("ductape").joinpath("samples.csv").read_text()
    with open(Path(directory) / "samples.csv", "w") as f:
        f.write(samplesheet)

    logger.info(f"Pipeline directory {directory} created")
    logger.info(
        f'Edit {directory}/ductape.yaml and run "cd {directory} && ductape run" to start the analysis',
    )
