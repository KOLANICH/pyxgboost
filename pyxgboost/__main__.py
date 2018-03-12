from plumbum import cli
from .compiler import *

class PyXGBoostCLI(cli.Application):
	"""Compiles an XGBoost model into python source and outputs it into stdout"""
	#generateMetadata=cli.Flag("--generate-metadata", default=False, help="Generate docstrings with metadata extracted from the model file")
	useNumPy=cli.Flag("--numpy", help="use numpy for vector operations")
	useSigmoids=cli.Flag("--sigmoids", help="use sigmoid functions for splits. This is meant to allows the gradients to be automatically computed.")
	def main(self, file:cli.ExistingFile):
			print(compile(file, useSigmoids=self.useSigmoids, useNumPy=self.useNumPy))

if __name__ == "__main__":
	PyXGBoostCLI.run()
