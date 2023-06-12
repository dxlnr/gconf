import copy
import dataclasses
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

import numpy as np
import yaml


@dataclass
class Conf(object):
    r"""
    Base configuration class.

    :param NAME: Name the configurations.
        Useful if your code needs to do things differently depending on which experiment is running.
    """
    NAME: str = None
    GENERIC_DICT: Dict[int, str] = field(
        default_factory=lambda: copy.copy(
            {
                0: "generic",
            }
        )
    )
    GENERIC_LIST: List[int] = field(default_factory=lambda: [4, 8, 16, 32, 64])
    GENERIC_TUPLE: Tuple[int] = field(
        default_factory=lambda: (32, 64, 128, 256, 512)
    )

    def __post_init__(self):
        # self._reset_params_after_merge()
        pass

    def merge_from_file(self, str_obj):
        """Load a config from a YAML string encoding."""
        with open(str_obj, "r") as yf:
            try:
                cfg_as_dict = yaml.safe_load(yf)
                self._merge_a_into_self(cfg_as_dict, self, [])
                self._reset_params_after_merge()
            except yaml.YAMLError as exc:
                print(exc)

    def __iter__(self):
        """Create an iterator."""
        yield self.__dataclass_fields__

    def __setitem__(self, key, value):
        """Sets the value of self[key] from the object or instance of the class."""
        setattr(self, key, value)

    def __getitem__(self, key):
        """Evaluate the value of self[key] by the object or instance of the class."""
        return getattr(self, key)

    def __str__(self) -> str:
        """Custom output string."""
        s = "\n".join(
            f"  {field.name}: {getattr(self, field.name)!r}"
            for field in dataclasses.fields(self)
            if not field.name.startswith("__")
        )
        return f"Configurations:\n{s}\n"

    def _reset_params_after_merge(self):
        """Adjust parameters after the merge."""
        pass

    def _merge_a_into_self(self, external_d, cfg, key_list: List[str]):
        """Merge a config dictionary a into self, clobbering the
        options in b whenever they are also specified in a.

        :param external_d: External dictionary extracted from .yaml.
        :param conf: Config object that should be merged into.
        """
        for k, v_ in external_d.items():
            v = copy.deepcopy(v_)

            if hasattr(cfg, k):
                v = self._check_and_coerce_conf_value_type(v, cfg[k])
                cfg[k] = v

    @staticmethod
    def _check_and_coerce_conf_value_type(
        replacement,
        original,
        casts: List[List[Any]] = [[(tuple, list), (list, tuple)]],
        valid_types: Dict = {tuple, list, dict, str, int, float, bool, type(None)},
    ):
        """Checks that `replacement`, which is intended to replace `original` is of
        the right type. The type is correct if it matches exactly or is one of a few
        cases in which the type can be easily coerced.

        :param replacement: Intended replacement parameter.
        :param original: Value to be replaced.
        :param casts: List

        """
        original_type = type(original)
        replacement_type = type(replacement)

        if replacement_type == original_type:
            return replacement

        if (replacement_type == type(None) and original_type in valid_types) or (
            original_type == type(None) and replacement_type in valid_types
        ):
            return replacement

        # Cast replacement from from_type to to_type if the replacement and original
        # types match from_type and to_type
        def conditional_cast(from_type, to_type):
            if replacement_type == from_type and original_type == to_type:
                return True, to_type(replacement)
            else:
                return False, None

        for cast_pair in casts:
            for (from_type, to_type) in cast_pair:
                converted, converted_value = conditional_cast(from_type, to_type)
                if converted:
                    return converted_value

        raise ValueError(
            f"Type mismatch ({original_type} vs. {replacement_type}) with values ({original} vs. {replacement}) for Conf."
        )
