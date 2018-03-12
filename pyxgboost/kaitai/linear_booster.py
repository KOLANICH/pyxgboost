# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

from .pas_str import PasStr
from .f4_arr import F4Arr
class LinearBooster(KaitaiStruct):
    """gradient boosted linear model.
    
    .. seealso::
       Source - https://github.com/dmlc/xgboost/blob/master/src/gbm/gblinear_model.h#L49L58
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.param = self._root.Param(self._io, self, self._root)
        self.weight = F4Arr(self._io)

    class Reserved(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.zero = []
            i = 0
            while not self._io.is_eof():
                self.zero = self._io.ensure_fixed_contents(b"\x00")
                i += 1



    class Param(KaitaiStruct):
        """model parameter.
        
        .. seealso::
           Source - https://github.com/dmlc/xgboost/blob/master/src/gbm/gblinear_model.h#L15L33
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_feature = self._io.read_u4le()
            self.num_output_group = self._io.read_u4le()
            self._raw_reserved = self._io.read_bytes((32 * 4))
            io = KaitaiStream(BytesIO(self._raw_reserved))
            self.reserved = self._root.Reserved(io, self, self._root)


    class TrainParam(KaitaiStruct):
        """
        .. seealso::
           Source - https://github.com/dmlc/xgboost/blob/master/src/gbm/gblinear.cc#L25L46
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.updater = PasStr(self._io)
            self.debug_verbose = self._io.read_s4le()
            self.tolerance = self._io.read_f4le()



