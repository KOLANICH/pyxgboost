#!/usr/bin/env python3
import sys
from pathlib import Path
import unittest

def getTestsDir() -> Path:
	try:
		return Path(__file__).parent.absolute()
	except:
		return Path(".").absolute() / "tests"

testsDir=getTestsDir()
parentDir=testsDir.parent.absolute()
sys.path.insert(0, str(parentDir))
testModelsDir = testsDir / "models"
modelFileName="random.model"
modelPath=testModelsDir/modelFileName

from collections import OrderedDict
dict=OrderedDict

import pyxgboost
import pyxgboost.compiler
from pyxgboost.setuptoolsHelper import pyxgboostHelper

from os import urandom
import struct

def randomNumbers(count):
	bytes=urandom(count*4)
	return struct.unpack("f"*count, bytes)

def randomDataset(vectorCount, vectorLen):
	import numpy as np
	return np.random.rand(vectorCount, vectorLen)

#WARNING: with other hyperparams it may choose another path in the tree, need to investigate this
hyperparams={
	"colsample_bytree" : 0.9451615772532829,
	"learning_rate" : 0.44981231171492403,
	"max_depth" : 22,
	"min_child_weight" : 0.07894413336299037,
	"min_split_loss" : 0.7796040450315559,
	"n_estimators" : 20,
	"reg_alpha" : 0.0170901963375754,
	"subsample" : 0.9654030894680347
}

def randomModel(vectorCount=1000, vectorLen=100):
	import numpy as np
	import xgboost
	ds=randomDataset(vectorCount, vectorLen)
	targetResult=np.random.rand(vectorCount, vectorLen)
	dm=xgboost.DMatrix(ds, label=targetResult)
	return xgboost.train(hyperparams, dm, 10)

class Tests(unittest.TestCase):
	def setUp(self):
		import xgboost
		self.vectorLen=1000
		vectorCount=1000
		self.model=randomModel(vectorCount=vectorCount, vectorLen=self.vectorLen)
		testModelsDir.mkdir(exist_ok=True)
		self.model.save_model(str(modelPath))
	
	def tearDown(self):
		modelPath.unlink()
		
	def testInference(self):
		import xgboost
		import numpy as np
		testVec=randomNumbers(self.vectorLen)
		resXGBoost=self.model.predict(xgboost.DMatrix(np.array([testVec])))[0]
		modelBinary=self.model.save_raw()
		
		for useSigmoids, errorThreshold in ((False, 0.0001), (True, 0.001)):
			for useNumPy in (False, True):
				with self.subTest(useSigmoids=useSigmoids):
					with self.subTest(useNumPy=useNumPy):
						regress=pyxgboost.compiler.compile(modelBinary, pyxgboost.compiler.OutputType.func, useSigmoids=useSigmoids, useNumPy=useNumPy)
						resPyXGBoost=regress(testVec)[0]
						
						mean=(resPyXGBoost+resXGBoost)/2
						diff=np.abs(resPyXGBoost-resXGBoost)
						err=diff/mean
						print(err)
						self.assertTrue( err < errorThreshold)
	
	def testHelper(self):
		testCfg={
			"pyxgboost":{
				"models":{},
				"outputDir": testsDir / "output",
				"inputDir": testModelsDir,
				"search": True
			}
		}
		pyxgboostHelper(None, None, testCfg["pyxgboost"])
	

if __name__ == '__main__':
	unittest.main()
