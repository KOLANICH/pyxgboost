pyxgboost [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===============
[wheel](https://gitlab.com/KOLANICH/pyxgboost/-/jobs/artifacts/master/raw/wheels/pyxgboost-0.CI-py3-none-any.whl?job=build)
[![PyPi Status](https://img.shields.io/pypi/v/pyxgboost.svg)](https://pypi.python.org/pypi/pyxgboost)
![GitLab Build Status](https://gitlab.com/KOLANICH/pyxgboost/badges/master/pipeline.svg)
[![TravisCI Build Status](https://travis-ci.org/KOLANICH/pyxgboost.svg?branch=master)](https://travis-ci.org/KOLANICH/pyxgboost)
[![Coveralls Coverage](https://img.shields.io/coveralls/KOLANICH/pyxgboost.svg)](https://coveralls.io/r/KOLANICH/pyxgboost)
![GitLab Coverage](https://gitlab.com/KOLANICH/pyxgboost/badges/master/coverage.svg)
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/pyxgboost.svg)](https://libraries.io/github/KOLANICH/pyxgboost)

This is a tool for conversion an [`xgboost`](https://github.com/dmlc/xgboost)[![TravisCI Build Status](https://travis-ci.org/dmlc/xgboost.svg?branch=master)](https://travis-ci.org/dmlc/xgboost)![License](https://img.shields.io/github/license/dmlc/xgboost.svg) tree into python AST or source.

The parsers residing in [```kaitai``` dir](https://github.com/KOLANICH/pyxgboost/tree/master/pyxgboost/kaitai) are generated from [Kaitai Struct](https://github.com/kaitai-io/kaitai_struct) [definitions](https://github.com/KOLANICH/kaitai_struct_formats/tree/xgboost/scientific/data_science/dmlc) and since that have [Apache license](https://github.com/KOLANICH/pyxgboost/tree/master/pyxgboost/kaitai).

Requirements
------------
* [```Python 3```](https://www.python.org/downloads/). [```Python 2``` is dead, stop raping its corpse.](https://python3statement.org/) Use ```2to3``` with manual postprocessing to migrate incompatible code to ```3```. It shouldn't take so much time.

* [```kaitaistruct```](https://github.com/kaitai-io/kaitai_struct_python_runtime)
  [![PyPi Status](https://img.shields.io/pypi/v/kaitaistruct.svg)](https://pypi.python.org/pypi/kaitaistruct)
  ![License](https://img.shields.io/github/license/kaitai-io/kaitai_struct_python_runtime.svg) as a runtime for Kaitai Struct-generated code
  
* some of the AST-to-source conversion libraries: [`astor`](https://github.com/berkerpeksag/astor)[![PyPi Status](https://img.shields.io/pypi/v/astor.svg)](https://pypi.python.org/pypi/astor)[![TravisCI Build Status](https://travis-ci.org/berkerpeksag/astor.svg?branch=master)](https://travis-ci.org/berkerpeksag/astor)![License](https://img.shields.io/github/license/berkerpeksag/astor.svg), [`codegen`](https://github.com/andreif/codegen)[![PyPi Status](https://img.shields.io/pypi/v/codegen.svg)](https://pypi.python.org/pypi/codegen)[![TravisCI Build Status](https://travis-ci.org/andreif/codegen.svg?branch=master)](https://travis-ci.org/andreif/codegen)![License](https://img.shields.io/github/license/andreif/codegen.svg), [`astunparse`](https://github.com/simonpercivall/astunparse)[![PyPi Status](https://img.shields.io/pypi/v/astunparse.svg)](https://pypi.python.org/pypi/astunparse)[![TravisCI Build Status](https://travis-ci.org/simonpercivall/astunparse.svg?branch=master)](https://travis-ci.org/simonpercivall/astunparse)![License](https://img.shields.io/github/license/simonpercivall/astunparse.svg) and [`astmonkey`](https://github.com/mutpy/astmonkey)[![PyPi Status](https://img.shields.io/pypi/v/astmonkey.svg)](https://pypi.python.org/pypi/astmonkey)[![TravisCI Build Status](https://travis-ci.org/mutpy/astmonkey.svg?branch=master)](https://travis-ci.org/mutpy/astmonkey)![License](https://img.shields.io/github/license/mutpy/astmonkey.svg).

* [```plumbum```](https://github.com/tomerfiliba/plumbum)
  [![PyPi Status](https://img.shields.io/pypi/v/plumbum.svg)](https://pypi.python.org/pypi/plumbum)
  [![TravisCI Build Status](https://travis-ci.org/tomerfiliba/plumbum.svg?branch=master)](https://travis-ci.org/tomerfiliba/plumbum)
 ![License](https://img.shields.io/github/license/tomerfiliba/plumbum.svg) - for command line interface

