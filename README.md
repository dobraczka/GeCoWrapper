# Wrapper for GeCo data Generator and Corruptor

This repository contains a wrapper to make use of the corruption functions of ['GeCo - An online personal data Generator and Corruptor'](https://openresearch-repository.anu.edu.au/handle/1885/28255) by Tran, Khoi-Nguyen; Vatsalan, Dinusha; Christen, Peter

## Setup
The script `setupGeCo.sh` will [download](https://dmm.anu.edu.au/geco/),unpack and setup GeCo to make this wrapper work.

You also need `unicodecsv`, which can be installed using:

`pip install unicodecsv`

## Usage
Input files need to have `id` as first column.

```
usage: wrapper.py [-h] input_path output_path config_path [encoding]

positional arguments:
  input_path   path where the file is located that contains the data that is
               to be corrupted
  output_path  path where the corrupted file should be written
  config_path  path where the config is located
  encoding     path where the config is located

optional arguments:
  -h, --help   show this help message and exit
```

## Example
`python wrapper.py example/input.csv example/output.csv example/config.json`
