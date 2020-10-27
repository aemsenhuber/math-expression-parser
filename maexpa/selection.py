# Library selection for MaExPa.
#
# Copyright 2020 Alexandre Emsenhuber
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class Selection( object ):
	def __init__( self ):
		self._var = None
		self._func = None

	def __call__( self, name ):
		if name == None:
			# No variables or functions

			self._var = None
			self._func = None
		elif name == "std":
			# Python's standard library
			from . import callback_std

			self._var = callback_std.var
			self._func = callback_std.func
		elif name == "numpy":
			# NumPy
			from . import callback_numpy

			self._var = callback_numpy.var
			self._func = callback_numpy.func
		else:
			raise Exception( "Invalid value passed to maexpa.use(): {:s}".format( name ) )

	def get_var_cb( self ):
		return self._var

	def get_func_cb( self ):
		return self._func
