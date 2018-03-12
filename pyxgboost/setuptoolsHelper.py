#setuptools_kaitai
import os
from pathlib import Path
from .compiler import compile, OutputType
from .validator import validator, schema

def empty(o, k):
	return k not in o or not o[k]

def prepareCfg(cfg):
	if empty(cfg, "search"):
		cfg["search"]=schema["properties"]["search"]["default"]
	
	validator.check_schema(cfg)
	validator.validate(cfg)
	
	cfg["inputDir"]=Path(cfg["inputDir"])
	if empty(cfg, "outputDir"):
		cfg["outputDir"]=cfg["inputDir"]
	cfg["outputDir"]=Path(cfg["outputDir"])
	
	if cfg["search"]:
		for file in cfg["inputDir"].glob("*.model"):
			cfg["models"][cfg["outputDir"] / file.parent.relative_to(cfg["inputDir"]) / (file.stem+".py")]=file
	
	newFormats=type(cfg["models"])(cfg["models"])
	
	for target, ifp in cfg["models"].items():
		if not isinstance(target, Path):
			del(newFormats[target])
			newFormats[cfg["outputDir"]/target]=ifp
	cfg["models"]=newFormats
	
	for target, ifp in cfg["models"].items():
		if not isinstance(ifp, Path):
			cfg["models"][target]=cfg["inputDir"]/ifp
	
	validator.check_schema(cfg)
	validator.validate(cfg)

def pyxgboostHelper(dist, keyword, cfg:dict):
	prepareCfg(cfg)
	
	for ofp, ifp in cfg["models"].items():
		print("Compiling "+str(ifp)+" into "+str(ofp)+" ...")
		os.makedirs(str(ofp.parent), mode=0o440, exist_ok=True)
		with ofp.open("wt", encoding="utf-8") as of:
			of.write(compile(str(ifp), OutputType.source))
