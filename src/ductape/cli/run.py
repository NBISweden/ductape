"""
Run the pipeline

Some more explanation of what the run command does

Calls Snakemake to produce all the output files.

Any arguments that this wrapper script does not recognize are forwarded to Snakemake.
This can be used to provide file(s) to create, targets to run or any other Snakemake
options.

Run 'snakemake --help' or see the Snakemake documentation to see valid snakemake arguments.
"""
from importlib.resources import files, as_file
import logging
import subprocess
import sys
from pathlib import Path
import os

logger = logging.getLogger(__name__)


def add_arguments(parser):
    parser.add_argument(
        "--cores",
        "-c",
        metavar="N",
        type=int,
        help="Run on at most N CPU cores in parallel. Default: Use as many cores as available)",
    )
    parser.add_argument(
        "--profile",
        type=str,
        help="Run with this profile"
    )


def main(args, arguments):
    run_snakemake(**vars(args), arguments=arguments)


def run_snakemake(
    cores=None,
    profile=None,
    arguments=None,
):
    if profile:
        if os.path.exists(Path(profile, "config.yaml")):
            profile_dir = profile
            logger.debug(f"Running with profile {profile}")
        else:
            profile_config = files("ductape").joinpath(f"profiles/{profile}/config.yaml")
            print(profile_config)
            profile_dir = os.path.dirname(f"{profile_config}")
            if not os.path.exists(profile_dir):
                sys.exit(f"ERROR: Profile {profile} is unknown")
    source = files("ductape").joinpath("Snakefile")
    with as_file(source) as snakefile:
        command = [
            "snakemake",
            f"--cores={'all' if cores is None else cores}",
            "-s",
            snakefile,
        ]
        if profile:
            command += ["--profile", profile_dir]
        if arguments:
            command += arguments
        print(f"Running: {' '.join(str(c) for c in command)}")
        logger.debug("Running: %s", " ".join(str(c) for c in command))
        exit_code = subprocess.call(command)

    sys.exit(exit_code)
