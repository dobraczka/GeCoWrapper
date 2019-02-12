import json
from geco import corruptor
from geco import basefunctions


class CorruptionConfig:
    """ Contains all necessary configuration attributes to perform corruption """

    def __init__(
        self,
        num_dup_rec,
        max_dup_per_record,
        num_dup_distribution,
        max_modification_per_attr,
        num_modification_per_record,
        unicode_encoding,
    ):
        self.num_dup_rec = num_dup_rec
        self.max_dup_per_record = max_dup_per_record
        self.num_dup_distribution = num_dup_distribution
        self.max_modification_per_attr = max_modification_per_attr
        self.num_modification_per_record = num_modification_per_record
        self.unicode_encoding = unicode_encoding
        self.corruptors = None
        self.mod_prob_dict = None
        self.attribute_mod_dict = None

    @classmethod
    def read(self, file_path):
        config = None
        with open(file_path) as f:
            data = json.load(f)
            config = CorruptionConfig(
                data["num_dup_rec"],
                data["max_dup_per_record"],
                str(data["num_dup_distribution"]),
                data["max_modification_per_attr"],
                data["num_modification_per_record"],
                str(data["unicode_encoding"]),
            )
            config.corruptors = config.get_corruptors(data["corruptors"])
            config.attribute_mod_dict, config.mod_prob_dict = config.get_attributes(
                data["attributes"], config.corruptors
            )
        return config

    def position_mod(self, pos_string):
        if pos_string == "normal":
            return corruptor.position_mod_normal
        elif pos_string == "uniform":
            return corruptor.position_mod_uniform
        print("Unknown position mode!")
        return None

    def get_edit_corruptor(self, obj):
        return corruptor.CorruptValueEdit(
            position_function=self.position_mod(obj["position_function"]),
            char_set_funct=basefunctions.char_set_ascii,
            insert_prob=obj["insert_prob"],
            delete_prob=obj["delete_prob"],
            substitute_prob=obj["substitute_prob"],
            transpose_prob=obj["transpose_prob"],
        )

    def get_ocr_corruptor(self, obj):
        return corruptor.CorruptValueOCR(
            position_function=self.position_mod(obj["position_function"]),
            lookup_file_name=str(obj["lookup_file_name"]),
            has_header_line=obj["has_header_line"] == "True",
            unicode_encoding=self.unicode_encoding,
        )

    def get_categorical_corruptor(self, obj):
        return corruptor.CorruptCategoricalValue(
            lookup_file_name=str(obj["lookup_file_name"]),
            has_header_line=obj["has_header_line"] == "True",
            unicode_encoding=self.unicode_encoding,
        )

    def get_keyboard_corruptor(self, obj):
        return corruptor.CorruptValueKeyboard(
            position_function=self.position_mod(obj["position_function"]),
            row_prob=obj["row_prob"],
            col_prob=obj["col_prob"],
        )

    def get_phonetic_corruptor(self, obj):
        return corruptor.CorruptValuePhonetic(
            lookup_file_name=str(obj["lookup_file_name"]),
            has_header_line=obj["has_header_line"] == "True",
            unicode_encoding=self.unicode_encoding,
        )

    def get_missing_corruptor(self, obj):
        if "missing_val" in obj:
            return corruptor.CorruptMissingValue(missing_val=obj["missing_val"])
        elif "missing_value" in obj:
            return corruptor.CorruptMissingValue(missing_value=obj["missing_value"])
        else:
            return corruptor.CorruptMissingValue()

    def get_corruptors(self, corrs):
        corruptors = {}
        for c in corrs:
            for name in c:
                ctype = c[name]["type"]
                if ctype == "Edit":
                    corruptors[name] = self.get_edit_corruptor(c[name])
                elif ctype == "OCR":
                    corruptors[name] = self.get_ocr_corruptor(c[name])
                elif ctype == "Categorical":
                    corruptors[name] = self.get_categorical_corruptor(c[name])
                elif ctype == "Keyboard":
                    corruptors[name] = self.get_keyboard_corruptor(c[name])
                elif ctype == "Phonetic":
                    corruptors[name] = self.get_phonetic_corruptor(c[name])
                elif ctype == "Missing":
                    corruptors[name] = self.get_missing_corruptor(c[name])
        return corruptors

    def get_attributes(self, attr, corrs):
        attribute_mod_dict = {}
        mod_prob_dict = {}
        # Iterate over attribute names
        for a in attr:
            attribute_mod_dict[a] = []
            # Iterate over corruptornames for attribute
            for c in attr[a]:
                if not "overall_prob" in c:
                    attribute_mod_dict[a].append((attr[a][c], corrs[c]))
                else:
                    mod_prob_dict[a] = attr[a][c]

        return attribute_mod_dict, mod_prob_dict
