import typing
import ast
from enum import IntEnum
from .kaitai.tree_booster import TreeBooster
from .kaitai.xgboost import Xgboost

if False and hasattr(ast, "Constant"):
	astNum=ast.Constant
	astStr=ast.Constant
	astNameConstant=ast.Constant
else:
	astNum=ast.Num
	astStr=ast.Str
	astNameConstant=ast.NameConstant

treesAccumulator=ast.Name(id="trees")
vector=ast.Name(id="vector")
res=ast.Name(id='res')
floatType=ast.Name(id='float')
rangeType=ast.Name(id='range')
enumerateFunc=ast.Name(id='enumerate')
lenFunc=ast.Name(id='len')
strFunc=ast.Name(id='str')
noneCnst=astNameConstant(value=None)
regressorFunctionName="predict"
#numpyArray=ast.Attribute(value=ast.Name(id='numpy'), attr='array')

def leaf(val:float, useExpression:bool) -> ast.Return:
	"""Creates AST nodes for a leaf"""
	res=astNum(n=val)
	if not useExpression:
		return ast.Return(value=res)
	else:
		return res

def missingCheck(check: ast.Compare, el: ast.Subscript, default: bool) -> ast.BoolOp:
	"""Creates AST nodes corresponding to check whether the `el` is None, if it is returns `default`"""
	return ast.BoolOp(op=(ast.Or() if default else ast.And()), values=[
		ast.Compare(left=el, ops=[(ast.Is() if default else ast.IsNot())], comparators=[noneCnst]),
		check
	])

tanhName='tanh'
def tanhCall(arg):
	return ast.Call(
		func=ast.Name(tanhName),
		args=[arg],
		keywords=[]
	)

#globalInvTemp=ast.Num(n=100)
inverseTemperatureArgName="iT"
globalInvTemp=ast.Name(inverseTemperatureArgName)
sigmoidSplitFuncName="s"
def generateFermiSplitFunction(funcName, tanhModuleName='math'):
	marginArgName="margin"
	lesArgName="les"
	lesArg=ast.Name(id=lesArgName)
	greatArgName="gret"
	valueArgName="val"
	
	yield ast.ImportFrom(module=tanhModuleName, names=[ast.alias(name=tanhName, asname=None)], level=0)
	yield ast.Assign(targets=[globalInvTemp], value=astNum(n=100))
	yield ast.FunctionDef(
		name=funcName,
		args=ast.arguments(args=[
			ast.arg(arg=valueArgName, annotation=floatType),
			ast.arg(arg=marginArgName, annotation=floatType),
			ast.arg(arg=lesArgName, annotation=floatType),
			ast.arg(arg=greatArgName, annotation=floatType),
			ast.arg(arg=inverseTemperatureArgName, annotation=floatType)
		], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]),
		body=[
			ast.Return(
				value=ast.BinOp(
					left=lesArg,
					op=ast.Add(),
					right=ast.BinOp(
						left=ast.BinOp(
							left=astNum(n=0.5),
							op=ast.Mult(),
							right=ast.BinOp(
								left=tanhCall(
									ast.BinOp(
										left=ast.BinOp(
											left=ast.Name(id=valueArgName),
											op=ast.Sub(),
											right=ast.Name(id=marginArgName)
										),
										op=ast.Mult(),
										right=globalInvTemp
									)
								), op=ast.Add(), right=astNum(n=1)
							)
						),
						op=ast.Mult(),
						right=ast.BinOp(left=ast.Name(id=greatArgName), op=ast.Sub(), right=lesArg)
					)
				)
			)
		],
		decorator_list=[], returns=floatType
	)

import astor
def generateSplit(varId:int, margin:float, les:ast.stmt, gret:ast.stmt, defaultLeft:bool, useSigmoids:bool) -> ast.If:
	"""Creates AST nodes corresponding to tree splits"""
	el=ast.Subscript(
		value=vector,
		slice=ast.Index(
			value=astNum(n=varId)
		)
	)
	if not useSigmoids:
		check=ast.Compare(
			left=el,
			comparators=[astNum(margin)],
			ops=[
				ast.Lt()
			]
		)
		check=missingCheck(check, el, defaultLeft)
		return (ast.If(
		#return ast.Expr(value=ast.IfExp(
			test=check,
			body=[
				les
			],
			orelse=[
				gret
			]
		))
	else:
		return ast.Call(func=ast.Name(id=sigmoidSplitFuncName), args=[el, astNum(margin), les, gret, globalInvTemp], keywords=[])

def findRoots(nodes: typing.Iterable[TreeBooster.RegTree.Node], count: int) -> typing.Iterator[TreeBooster.RegTree.Node]:
	"""Finds tree roots"""
	c=0
	for node in nodes:
		if node.is_root:
			c+=1
			yield node
			if c>=count:
				break

def dfs(nodes:typing.Iterable[TreeBooster.RegTree.Node], root:TreeBooster.RegTree.Node, useSigmoids:bool) -> typing.Union[ast.Return, ast.If]:
	"""Walks the tree with root `root` and builds if-else AST control flow tree"""
	def dfs_(node):
		if node.is_leaf:
			return leaf(node.leaf_value, useExpression=useSigmoids)
		else:
			return generateSplit(node.split_index, node.split_cond, dfs_(node.left), dfs_(node.right), defaultLeft=node.default_left, useSigmoids=useSigmoids)
	ress=dfs_(root)
	if useSigmoids:
		ress=ast.Return(value=ress)
	return ress

#treeArgT=ast.Tuple(elts=[numpyArray, ast.Name(id='list')])
treeArgT=ast.Name(id='list')
def wrapWithFunc(body: typing.Iterable[ast.stmt], name: typing.Optional[str] = None) -> ast.FunctionDef:
	"""Wraps an AST into function."""
	if name is None:
		ctor=ast.Lambda
	else:
		ctor=ast.FunctionDef
	return ctor(
		name = name,
		args = ast.arguments(
			args = [
				ast.arg(arg = vector.id, annotation = treeArgT)
			],
			vararg=None,
			kwonlyargs=[],
			kw_defaults=[],
			kwarg=None,
			defaults=[]
		),
		body = body,
		decorator_list = [],
		returns = floatType
	)

def treesToFuncs(tree: TreeBooster.RegTree, name: typing.Optional[str] = None, useSigmoids:bool=False) -> typing.Iterator[ast.FunctionDef]:
	"""Converts a decision tree into a function"""
	for root in findRoots(tree.nodes, tree.param.num_roots):
		res=wrapWithFunc([
			ast.Expr(value=astStr(s=genTreeSummary(tree))),
			dfs(tree.nodes, root, useSigmoids)
		], name)
		#print(astor.to_source(res))
		yield res

def genModelSummary(model: Xgboost) -> str:
	"""Generates a docstring for a model"""
	res=[
		"model: "+str(model.name_gbm_.str),
		"objective: "+str(model.name_obj_.str),
		"base score: "+str(model.param.base_score),
		"features: "+str(model.param.num_feature),
		"classes: "+str(model.param.num_class),
		
	]
	if model.name_gbm_.str != "linear":
		res.extend((
			"output groups: "+str(model.gbm_.param.num_output_group),
			"roots: "+str(model.gbm_.param.num_roots),
			"trees: "+str(model.gbm_.param.num_trees),
			"leaf vector size: "+str(model.gbm_.param.size_leaf_vector),
		))
	if model.param.contain_extra_attrs:
		res.extend((p[0].str+": "+p[1].str for p in model.attributes_))
	return "\n".join(res)

def genTreeSummary(tree: TreeBooster.RegTree) -> str:
	"""Generates a docstring for a single tree"""
	res=[
		"roots: "+str(tree.param.num_roots),
		"nodes: "+str(tree.param.num_nodes)+" ("+str(tree.param.num_deleted)+" deleted)",
		"depth: "+str(tree.param.max_depth),
		"features: "+str(tree.param.num_feature),
		"leaf vector size: "+str(tree.param.size_leaf_vector),
	]
	return "\n".join(res)

treesCountSym=ast.Name(id='treesCount')
groupTemp=ast.Name(id='group')
treeTemp=ast.Name(id='tree')
numpySumName='sum'
numpySum=ast.Name(id=numpySumName)
groupCounter=ast.Name(id='j')

def makeGroup(name, base_score, useNumPy=None):
	groupTemp=ast.Subscript(value=treesAccumulator, slice=ast.Index(value=ast.Name(name)))
	code=[]
	res=ast.Name(id='res')
	baseScore=astNum(n=base_score)
	treeCall=ast.Call(func=treeTemp, args=[vector], keywords=[])
	iterArgDict={
		"target":treeTemp,
		"iter":groupTemp,
	}
	
	if not useNumPy:
		code.append(ast.Assign(targets=[res], value=baseScore))
		code.append(
			ast.For(
				body=[
					ast.AugAssign(
						target=res,
						op=ast.Add(),
						value=treeCall
					)
				],
				orelse=[],
				**iterArgDict,
			)
		)
	else:
		res=ast.BinOp(
			left=baseScore,
			op=ast.Add(),
			right=ast.Call(
				func=numpySum,
				args=[
					ast.ListComp(
						elt=treeCall,
						generators=[ast.comprehension(
							ifs=[],
							**iterArgDict,
						)]
					)
				],
				keywords=[]
			)
		)
	code.append(ast.Return(res))
	return wrapWithFunc(code, name)

def makeRegressor(model:Xgboost, useSigmoids:bool=False, useNumPy:bool=False) -> ast.Module:
	"""Converts a regression XGBoost decision tree model into a python module of if-else trees"""
	#code:typing.List[ast.stmt]=[]
	code=[]
	numpyModuleName="numpy"
	if useSigmoids:
		code.extend(generateFermiSplitFunction(sigmoidSplitFuncName, tanhModuleName=(numpyModuleName if useNumPy else "math")))
	
	if useNumPy:
		code.append(ast.ImportFrom(module=numpyModuleName, names=[ast.alias(name=numpySumName, asname=None)], level=0))
	
	features=int(model.param.num_feature)
	trees=int(model.gbm_.param.num_trees)
	groups=int(model.gbm_.param.num_output_group)
	treesInAGroup=trees//groups
	
	groupFunctions=[]
	groupFunctionsNames=[]
	elts=[]
	for j in range(groups):
		group=[]
		for i in range(treesInAGroup):
			t=model.gbm_.trees[j*treesInAGroup+i]
			name="g"+str(j)+"_t"+str(i)
			code.extend(treesToFuncs(t, name, useSigmoids))
			group.append(ast.Name(id=name))
		elts.append(ast.Tuple(elts=group))
		groupFuncName="g"+str(j)
		groupFunctionsNames.append(ast.Name(groupFuncName))
		groupFunctions.append(makeGroup(groupFuncName, model.param.base_score, useNumPy=useNumPy))
	
	code.extend(groupFunctions)
	code.append(ast.Assign(targets=[treesAccumulator], value=ast.Dict(keys=groupFunctionsNames, values=elts)))
	
	code.append(
		wrapWithFunc(
			[
				ast.Expr(value=astStr(s=genModelSummary(model))),
				ast.Assert(
					test=ast.Compare(
						left=ast.Call(func=lenFunc, args=[vector], keywords=[]),
						ops=[ast.Eq()],
						comparators=[astNum(n=features)]
					),
					msg=ast.BinOp(
						left=ast.BinOp(
							left=astStr(s="This model requires exactly "+str(features)+" feature, but "),
							op=ast.Add(),
							right=ast.Call(func=strFunc, args=[ast.Call(func=lenFunc, args=[vector], keywords=[])], keywords=[])
						),
						op=ast.Add(),
						right=astStr(s=" were given")
					)
				),
				ast.Assign(targets=[res],
					value=ast.ListComp(
						elt=ast.Call(func=groupTemp, args=[vector], keywords=[]),
						generators=[ast.comprehension(
							target=groupTemp,
							iter=treesAccumulator,
							ifs=[]
						)]
					)
				),
				ast.Return(value=res)
			],
			regressorFunctionName
		)
	)
	
	return ast.Module(body=code)
