import base64
import calendar
import datetime
import itertools
import re
import zlib
from typing import Any, Callable, Dict, Iterator, Tuple, Union

import numpy as np

try:
    from importlib.resources import files

    def get_resource_path(package, resource_name) -> str:
        """
        Workaround for 3.8 - 3.12+ compatibility. Returns the resource path

        :param package: The package name (pass __package__)
        :param resource_name: The name of the resource (file name)
        :return: Full resource path of the file
        """
        return str(files(package).joinpath(resource_name))

except ImportError:
    from pkg_resources import resource_filename

    def get_resource_path(package, resource_name) -> str:
        """
        Workaround for 3.8 - 3.12+ compatibility. Returns the resource path

        :param package: The package name (pass __package__)
        :param resource_name: The name of the resource (file name)
        :return: Full resource path of the file
        """
        return resource_filename(package, resource_name)


def dt_epoch_msecs(value: Union[datetime.date, datetime.datetime]) -> float:
    """
    Calculate miliseconds since epoch start for python datetimes.
    """
    return int(calendar.timegm(value.timetuple())) * 1000


def np_dt_epoch_msec(value: np.datetime64) -> float:
    """
    Calculate miliseconds since epoch start for numpy datetimes.
    """
    return value.astype(int) / 1000


def encode_string(string: str, level: int = 9) -> bytes:
    """
    Compresses and base64 encodes the supplied string

    :param string: String to encode and compress
    :param level: Compression level
    :return: Compressed and encoded string
    """
    return base64.b64encode(zlib.compress(string.encode("utf-8"), level)[2:-4])


def camelcase(value: str) -> str:
    """
    Converts 'under_score_string' -> 'underScoreString'

    :param value: Underscore separated string
    :return: CamelCased string
    """
    rest = value.split("_")
    return rest[0] + "".join(word.title() for word in rest[1:])


def underscorecase(camelcased: str) -> str:
    """
    Converts 'underScoreString' -> 'under_score_string'

    :param value: CamelCased string
    :return: Underscore separated string
    """
    return re.sub("([A-Z]+)", r"_\1", camelcased).lower()


def cfg_to_prop_string(
    cfg: "Cfg",
    key_transform: Callable[[str], str] = lambda k: k,
    value_transform: Callable[[str], str] = lambda v: v,
    separator: str = ";",
) -> str:
    """
    Convert the config object to a property string. Useful for constructing CSS and javascript
    object init strings.

    Underscores are replaced with dashes and values are converted to lower case.
    """
    return separator.join([f"{key_transform(key)}:{value_transform(value)}" for key, value in cfg.items()])


def cfg_to_css_string(cfg: "Cfg") -> str:
    return cfg_to_prop_string(cfg, lambda k: k.replace("_", "-"), lambda v: str(v).lower())


class Cfg(dict):
    """
    A dict-like mapping for inheritable block parameters.
    """

    def inherit(self, parent: Union[dict, "Cfg"]) -> "Cfg":
        """
        Inherit all parent settings that the current config does not define.
        """
        return self.__class__(Cfg._mergedicts(self, parent, False))

    def inherit_many(self, *args: "Cfg", **kwargs: Any) -> "Cfg":
        """
        Inherit many settings at once.
        """
        inherit_collapsed = self._collapse_args(args, kwargs)
        return self.inherit(inherit_collapsed)

    def override(self, parent: Union[Dict, "Cfg"]) -> "Cfg":
        """
        Override all settings specified in the overrides.
        """
        return self.__class__(Cfg._mergedicts(self, parent, True))

    def override_many(self, *args: "Cfg", **kwargs: Any) -> "Cfg":
        """
        Override many settings at once.
        """
        override_collapsed = self._collapse_args(args, kwargs)
        return self.override(override_collapsed)

    @staticmethod
    def _collapse_args(args: Tuple["Cfg", ...], kwargs: Any) -> "Cfg":
        inherit_agg = Cfg(kwargs)
        for arg in args:
            # If we got a type as configuration, instantiate it
            if isinstance(arg, type):
                arg = arg()

            inherit_agg = inherit_agg.inherit(arg)
        return inherit_agg

    @staticmethod
    def _mergedicts(dict1: Dict, dict2: Dict, take_second: bool) -> Iterator:
        for k in set(itertools.chain(dict1.keys(), dict2.keys())):
            if k in dict1 and k in dict2:
                v1 = dict1[k]
                v2 = dict2[k]
                if isinstance(v1, dict) and isinstance(v2, dict):
                    # The merged sub-dict type should be the operand type based on take_second
                    ctor = v2.__class__ if take_second else v1.__class__
                    yield (k, ctor(Cfg._mergedicts(v1, v2, take_second)))
                else:
                    yield (k, v2 if take_second else v1)
            elif k in dict1:
                yield (k, dict1[k])
            else:
                yield (k, dict2[k])

    def __getattr__(self, item: str) -> Any:
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"'Cfg' object has no attribute '{item}'")

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value

    def __setstate__(self, state) -> None:
        for key in state:
            self[key] = state[key]

    def __getstate__(self) -> Dict[str, Any]:
        return {key: self[key] for key in self}
