# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

from .str_arr import StrArr
from .linear_booster import LinearBooster
from .tree_booster import TreeBooster
from .pas_str import PasStr
from .str_pair_arr import StrPairArr
class Xgboost(KaitaiStruct):
    """It is an xgboost tree model.
    
    .. seealso::
       Source - https://github.com/dmlc/xgboost/blob/master/src/learner.cc#L268L354
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.param = self._root.ModelParam(self._io, self, self._root)
        self.name_obj_ = PasStr(self._io)
        self.name_gbm_ = PasStr(self._io)
        _on = self.name_gbm_.str
        if _on == u"gblinear":
            self.gbm_ = LinearBooster(self._io)
        else:
            self.gbm_ = TreeBooster(self._io)
        if self.param.contain_extra_attrs != 0:
            self.attributes_ = StrPairArr(self._io)

        if self.name_obj_.str == u"count:poisson":
            self.max_delta_step_str = PasStr(self._io)

        if self.param.contain_eval_metrics != 0:
            self.metrics_ = StrArr(self._io)


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



    class ModelParam(KaitaiStruct):
        """training parameter for regression.
        
        .. seealso::
           Source - https://github.com/dmlc/xgboost/blob/master/src/learner.cc#L38L70
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.base_score = self._io.read_f4le()
            self.num_feature = self._io.read_u4le()
            self.num_class = self._io.read_u4le()
            self.contain_extra_attrs = self._io.read_u4le()
            self.contain_eval_metrics = self._io.read_u4le()
            self._raw_reserved = self._io.read_bytes((29 * 4))
            io = KaitaiStream(BytesIO(self._raw_reserved))
            self.reserved = self._root.Reserved(io, self, self._root)


    @property
    def max_delta_step(self):
        """maximum delta update we can add in weight estimation
        this parameter can be used to stabilize update
        default=0 means no constraint on weight delta
        
        .. seealso::
           param.h
        """
        if hasattr(self, '_m_max_delta_step'):
            return self._m_max_delta_step if hasattr(self, '_m_max_delta_step') else None

        if self.name_obj_.str == u"count:poisson":
            self._m_max_delta_step = int(self.max_delta_step_str.str)

        return self._m_max_delta_step if hasattr(self, '_m_max_delta_step') else None


