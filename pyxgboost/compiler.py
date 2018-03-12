from pathlib import Path
from .kaitai.xgboost import Xgboost
from . import makeRegressor, regressorFunctionName
from .kaitaiParseBase import kaitaiParseBase
from enum import IntEnum
import typing
from importlib import import_module

from alternativez import Alternativez, Alternative, Dependency
r=Alternativez([
	Alternative(Dependency("astor", "git+https://github.com/berkerpeksag/astor.git"), "to_source"),
	Alternative(Dependency("codegen", "git+https://github.com/andreif/codegen.git"), "to_source"),
	Alternative(Dependency("astunparse", "git+https://github.com/simonpercivall/astunparse.git"), "unparse"),
	Alternative(Dependency("astmonkey.visitors", "git+https://github.com/mutpy/astmonkey.git"), "to_source"),
])
to_source=r()

class OutputType(IntEnum):
	AST=0
	source=1
	compiled=2
	context=3
	func=4

modulesWhitelist={"math", "numpy", "autograd.numpy"}
funcsWhitelist={"tanh", "sum"}

pythonCompile=compile
def compile(sourceModel:typing.Union[Path, str, bytes], outputType:OutputType=OutputType.source, *args, useSigmoids=False, useNumPy=False, **kwargs):
	outputType=OutputType(outputType)
	if isinstance(sourceModel, (Path, str)):
		sourceModelPath = sourceModel
	else:
		sourceModelPath = ""
	
	mod=makeRegressor(kaitaiParseBase(Xgboost, sourceModel), useSigmoids=useSigmoids, useNumPy=useNumPy)
	if outputType is OutputType.AST:
		return mod
	s=to_source(mod, *args, **kwargs )
	if outputType == OutputType.source:
		return s
	compiled=pythonCompile(s, filename="xgboost model<"+str(sourceModelPath)+">", mode="exec")
	if outputType is OutputType.compiled:
		return compiled
	def importSurrogate(name, globals=None, locals=None, fromlist=(), level=0):
		if level==0 and name in modulesWhitelist and all((fn in funcsWhitelist for fn in fromlist)):
			mod=import_module(name)
			for fn in fromlist:
				globals[fn]=getattr(mod, fn)
			return mod
		else:
			raise ImportError("Importing anything except tanh from math is not allowed")
		
	
	resEnv={"__builtins__":{"list":list, "dict": dict, "float": float, "int": int, "str": str, "range":range, "enumerate":enumerate, "len":len, "AssertionError":AssertionError, "__import__":importSurrogate}}
	exec(compiled, resEnv, resEnv)
	if outputType is OutputType.context:
		return resEnv
	elif outputType is OutputType.func:
		return resEnv[regressorFunctionName]
	else:
		raise ValueError("It's impossible to reach here!")
