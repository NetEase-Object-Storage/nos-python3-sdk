# -*- coding:utf8 -*-

import sys

PY2 = sys.version_info[0] == 2

if PY2:
    string_types = str,

else:
    string_types = str, bytes
    map = map

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
