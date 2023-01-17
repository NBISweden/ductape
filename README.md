# DUCTAPE workflow wrapper

This tool wraps metagenomic workflows. Why? Because there are already lots of
well-written workflows out there, but depending on your use-case neither of them 
can single-handedly do all the things you want. 

Therefore `ductape` takes advantage of how Snakemake can integrate both
[foreign](https://snakemake.readthedocs.io/en/stable/snakefiles/foreign_wms.html)
and [native](https://snakemake.readthedocs.io/en/stable/snakefiles/modularization.html#modules) 
workflows. The idea is to extend the functionality of existing workflows without
adding yet another one to the mix. 

## Installation

### With conda
1. Install with `conda create -c bioconda -n ductape ductape` and activate the environment.
2. Run `ductape init pipelinedir` and change into the newly created
   directory `pipelinedir`.
3. Edit `ductape.yaml` and `samples.csv`.
4. Run `ductape run`.

### From GitHub
1. Clone this repository with `git clone git@github.com:NBISweden/ductape.git`
2. Set up a conda environment to use for installation: `conda create -n ductape python`
3. Install `ductape`: `python -m pip install .`

## ductaped workflows

So far `ductape` wraps the `nf-core/mag` workflow and extends it with eggNOG
annotations for each assembled group of samples.