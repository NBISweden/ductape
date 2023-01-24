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
import yaml

logger = logging.getLogger(__name__)


def parse_arguments(arguments):
    consume = False
    config = {}
    for item in arguments:
        if item == "--config":
            consume = True
            continue
        if consume:
            if item.startswith("--"):
                return config
            key, value = item.split("=")
            config[key] = value
    return config


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
        help="Run with this profile. Either a path to a directory with 'config.yaml' "
             "or one already installed in default location (e.g. ~/.config/snakemake "
             "depending on your system) or you may specify one of 'local', 'uppmax' "
             "or 'test'"
    )
    parser.add_argument(
        "--configfile",
        metavar="configfile",
        type=str,
        help="Config file to pass on to snakemake. Defaults to 'ductape.yaml' in current directory",
        default="ductape.yaml"
    )


def main(args, arguments):
    run_snakemake(**vars(args), arguments=arguments)


def run_snakemake(
    cores=None,
    profile=None,
    configfile=None,
    arguments=None,
):
    if not os.path.exists(configfile):
        sys.exit(f"ERROR: Configfile {configfile} does not exist\n")
    with open(configfile, 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)
    config.update(parse_arguments(arguments))
    if profile:
        if os.path.exists(Path(profile, "config.yaml")):
            profile_dir = profile
            logger.debug(f"Running with profile {profile}")
        else:
            profile_config = files("ductape").joinpath(f"profiles/{profile}/config.yaml")
            profile_dir = os.path.dirname(f"{profile_config}")
            if not os.path.exists(profile_config):
                sys.exit(f"ERROR: Profile {profile} is unknown")
        with open(Path(profile_dir, "config.yaml"), 'r') as yaml_file:
            profile_config = yaml.safe_load(yaml_file)
    else:
        profile_config = {}
    if "slurm" in profile_config.keys() and profile_config["slurm"] in ["True", True]:
        if "account" not in config.keys() or config["account"] == "":
            sys.exit(f"ERROR: '--slurm' set in profile but no slurm account given in {configfile}")
    source = files("ductape").joinpath("Snakefile")
    with as_file(source) as snakefile:
        command = [
            "snakemake",
            f"--cores={'all' if cores is None else cores}",
            "--configfile",
            configfile,
            "-s",
            snakefile,
        ]
        if profile:
            command += ["--profile", profile_dir]
        if arguments:
            command += arguments
        print(f"Running: {' '.join(str(c) for c in command)}")
        exit_code = subprocess.call(command)

    sys.exit(exit_code)
