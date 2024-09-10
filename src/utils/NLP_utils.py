import pkg_resources
import symspellpy

from symspellpy import SymSpell, Verbosity


class SpellingCorrectionModel:
    def __init__(self, max_dict_edit_dist: int = 2, prefix_length: int = 7, count_threshold: int = 1) -> None:
        self.max_dict_edit_dist = max_dict_edit_dist
        self.prefix_length = prefix_length
        self.count_threshold = count_threshold
        self.model = self._initialize_model()

    def _initialize_model(self) -> symspellpy.symspellpy.SymSpell:
        model = SymSpell(self.max_dict_edit_dist, self.prefix_length, self.count_threshold)
        dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
        bigram_dictionary_path = pkg_resources.resource_filename(
            "symspellpy", "frequency_bigramdictionary_en_243_342.txt"
        )
        model.load_dictionary(dictionary_path, term_index=0, count_index=1)
        model.load_bigram_dictionary(bigram_dictionary_path, term_index=0, count_index=2)
        return model

    def __call__(self, text: str) -> str:
        string: str = self.model.lookup_compound(text, max_edit_distance=self.max_dict_edit_dist)[0].term
        return string
