#!/bin/bash
wget https://dmm.anu.edu.au/geco/geco-data-generator-corruptor.tar.gz &&
tar xvzf geco-data-generator-corruptor.tar.gz &&
mv geco-data-generator-corruptor geco &&
touch geco/__init__.py
