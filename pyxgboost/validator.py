import json, jsonschema
from pathlib import Path

thisDir=Path(__file__).parent
with (thisDir / "config.schema.json").open("rt", encoding="utf-8") as f:
	schema=json.load(f)

def isPath(val):
	if isinstance(val, Path):
		return True
	elif isinstance(val, str):
		try:
			Path(val)
		except:
			return False
	return False

types={"function":callable, "path":isPath}
validator=jsonschema.Draft4Validator(schema, types=types)