import re
import zlib
import base64
import calendar
import itertools
import sys
from six import iterkeys, iteritems

if sys.version_info > (3,):
    long = int


def dt_epoch_msecs(value):
    """
    Calculate miliseconds since epoch start for python datetimes.
    """
    return long(calendar.timegm(value.timetuple())) * 1000


def np_dt_epoch_msec(value):
    """
    Calculate miliseconds since epoch start for numpy datetimes.
    """
    return value.astype(long) / 1000


def encode_string(string, level=9):
    """
    Compresses and base64 encodes the supplied string
    :param string: String to encode and compress
    :param level: Compression level
    :return: Compressed and encoded string
    """
    return base64.b64encode(zlib.compress(string.encode('utf8'), level)[2:-4])


def camelcase(value):
    """
    Converts 'under_score_string' -> 'underScoreString'

    :param value: Underscore separated string
    :return: CamelCased string
    """
    rest = value.split("_")
    return rest[0] + "".join(word.title() for word in rest[1:])


def underscorecase(camelcased):
    """
    Converts 'underScoreString' -> 'under_score_string'

    :param value: CamelCased string
    :return: Underscore separated string
    """
    return re.sub('([A-Z]+)', r'_\1', camelcased).lower()


def cfg_to_prop_string(cfg, key_transform=lambda k: k, value_transform=lambda v: v, separator=";"):
    """
    Convert the config object to a property string. Useful for constructing CSS and javascript
    object init strings.

    Underscores are replaced with dashes and values are converted to lower case.
    """
    return separator.join(["%s:%s" % (key_transform(key), value_transform(value)) for key, value in iteritems(cfg)])


def cfg_to_css_string(cfg):
    return cfg_to_prop_string(cfg, lambda k: k.replace("_", "-"), lambda v: str(v).lower())


class Cfg(dict):
    """
    Provides plumbing for inheritable block parameters.
    """

    def inherit(self, parent):
        """
        Inherit all parent settings that the current config does not define.
        """
        return self.__class__(Cfg._mergedicts(self, parent, False))

    def inherit_many(self, *args, **kwargs):
        """
        Inherit many settings at once.
        """
        inherit_collapsed = self._collapse_args(args, kwargs)
        return self.inherit(inherit_collapsed)

    def override(self, parent):
        """
        Override all settings specified in the overrides.
        """
        return self.__class__(Cfg._mergedicts(self, parent, True))

    def override_many(self, *args, **kwargs):
        """
        Override many settings at once.
        """
        override_collapsed = self._collapse_args(args, kwargs)
        return self.override(override_collapsed)

    @staticmethod
    def _collapse_args(args, kwargs):
        inherit_agg = Cfg(kwargs)
        for arg in args:
            # If we got a type as configuration, instantiate it
            if isinstance(arg, type):
                arg = arg()

            inherit_agg = inherit_agg.inherit(arg)
        return inherit_agg

    @staticmethod
    def _mergedicts(dict1, dict2, take_second):
        for k in set(itertools.chain(iterkeys(dict1), iterkeys(dict2))):
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

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, name, value):
        self[name] = value
