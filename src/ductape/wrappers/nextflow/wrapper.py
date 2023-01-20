__author__ = "John Sundh"
__copyright__ = "Copyright 2023, John Sundh"
__email__ = "john.sundh@scilifelab.se"
__license__ = "MIT"

from snakemake.shell import shell

revision = snakemake.params.get("revision")
resume = snakemake.params.get("resume", "")
profile = snakemake.params.get("profile", [])
extra = snakemake.params.get("extra", "")
nf_config = snakemake.params.get("nf_config", "")
sm_config = snakemake.params.get("sm_config")
envvars = snakemake.params.get("envvars", "")

if isinstance(profile, str):
    profile = [profile]

args = []

if revision:
    args += ["-revision", revision]
if profile:
    args += ["-profile", ",".join(profile)]
if resume:
    args += ["-resume"]
if nf_config:
    args += [f"-c {nf_config}"]
print(args)

# TODO pass threads in case of single job
# TODO limit parallelism in case of pipeline
# TODO handle other resources

add_parameter = lambda name, value: args.append("--{} {}".format(name, value))

for name, files in snakemake.input.items():
    if isinstance(files, list):
        # TODO check how multiple input files under a single arg are usually passed to nextflow
        files = ",".join(files)
    add_parameter(name, files)
if not nf_config:
    for name, value in sm_config.items():
        if name == "envvars":
            continue
        if value != "":
            add_parameter(name, value)
        else:
            add_parameter(name, "False")

log = snakemake.log_fmt_shell(stdout=False, stderr=True)
args = " ".join(args)
pipeline = snakemake.params.pipeline
if isinstance(envvars, str):
    envvars = f"export {';'.join(envvars)} &&"

shell("{envvars} nextflow run {pipeline} {args} {extra} {log}")
