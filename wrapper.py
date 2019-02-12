#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unicodecsv
import codecs
import sys
import argparse
from config_reader import CorruptionConfig
from geco import basefunctions
from geco import attrgenfunct
from geco import contdepfunct
from geco import generator
from geco import corruptor

rec_id_attr_name = "id"


def read_input_to_dict(input_path, encoding):
    rec_dict = {}
    attr_name_list = []
    with open(input_path, mode="r") as infile:
        reader = unicodecsv.reader(infile, encoding=encoding)
        attr_name_list = reader.next()[1:]  # get the header
        for row in reader:
            rec_dict[rec_id_attr_name + "-" + row[0]] = row[1:]
    return rec_dict, attr_name_list


def perform_corruption(input_path, output_path, config_file, encoding):
    rec_dict, attr_name_list = read_input_to_dict(input_path, encoding)
    config = CorruptionConfig.read(config_file)
    data_corruptor = corruptor.CorruptDataSet(
        number_of_org_records=len(rec_dict),
        number_of_mod_records=config.num_dup_rec,
        attribute_name_list=attr_name_list,
        max_num_dup_per_rec=config.max_dup_per_record,
        num_dup_dist=config.num_dup_distribution,
        max_num_mod_per_attr=config.max_modification_per_attr,
        num_mod_per_rec=config.num_modification_per_record,
        attr_mod_prob_dict=config.mod_prob_dict,
        attr_mod_data_dict=config.attribute_mod_dict,
    )
    rec_dict = data_corruptor.corrupt_records(rec_dict)
    # Write result
    with codecs.open(output_path, mode="w", encoding=encoding) as outfile:
        header = "id"
        for v in attr_name_list:
            header += "," + v
        outfile.write(header + "\n")
        for key in rec_dict:
            row = '"' + key + '"'
            for v in rec_dict[key]:
                row += ',"' + v + '"'
            outfile.write(row + "\n")


def main():
    global input_path
    global output_path
    global config_path
    global encoding
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_path",
        help="path where the file is located that contains the data that is to be corrupted",
    )
    parser.add_argument(
        "output_path", help="path where the corrupted file should be written"
    )
    parser.add_argument("config_path", help="path where the config is located")
    parser.add_argument(
        "encoding",
        nargs="?",
        default="utf-8",
        help="encoding if necessary, utf-8 is set as default",
    )
    args = parser.parse_args()
    perform_corruption(
        args.input_path, args.output_path, args.config_path, args.encoding
    )


if __name__ == "__main__":
    main()
