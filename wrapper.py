from geco import basefunctions
from geco import attrgenfunct
from geco import contdepfunct
from geco import generator
from geco import corruptor
import json
import unicodecsv
import codecs
from config_reader import CorruptionConfig

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


def perform_corruption(input_path, output_path, config_file, encoding="utf-8"):
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
    with codecs.open(output_path, mode="w", encoding="utf-8") as outfile:
        header = "id"
        for v in attr_name_list:
            header += "," + v
        outfile.write(header + "\n")
        for key in rec_dict:
            row = '"' + key + '"'
            for v in rec_dict[key]:
                row += ',"' + v + '"'
            outfile.write(row + "\n")


perform_corruption("/tmp/artists.csv", "/tmp/artists_corrupted.csv", "config.json")
