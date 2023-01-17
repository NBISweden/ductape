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

1. Install with `mamba create -n ductape ductape` and activate the environment.
2. Run `ductape init pipelinedir` and change into the newly created
   directory `pipelinedir`.
3. Edit `ductape.yaml` and `samples.csv`.
4. Run `ductape run`.

## ductaped workflows

So far `ductape` wraps the `nf-core/mag` workflow and extends it with eggNOG
annotations for each assembled group of samples.