# Mathematical functions and variables for MaExPa (NumPy version).
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

from . import exception

import math
import numpy

_func_defs = {
	"min": { "func": numpy.minimum, "args": 2 },
	"max": { "func": numpy.maximum, "args": 2 },
	"pow": { "func": numpy.power, "args": 2 },

	"abs": { "func": numpy.fabs, "args": 1 },
	"floor": { "func": numpy.floor, "args": 1 },
	"ceil": { "func": numpy.ceil, "args": 1 },

	"exp": { "func": numpy.exp, "args": 1 },
	"log": { "func": numpy.log, "args": 1 },
	"log2": { "func": numpy.log2, "args": 1 },
	"log10": { "func": numpy.log10, "args": 1 },

	"sqrt": { "func": numpy.sqrt, "args": 1 },
	"cbrt": { "func": numpy.cbrt, "args": 1 },
}

_var_defs = {
	"e": math.e,
	"pi": math.pi,
	"tau": math.tau,
}

def func( name, args ):
	'''
	Standard callback function to call methods in Python's math module.
	'''

	if not name in _func_defs:
		raise exception.NoFuncException( name )

	if len( args ) != _func_defs[ name ][ "args" ]:
		raise exception.FuncArgsNumException( name, _func_defs[ name ][ "args" ], len( args ) )

	return _func_defs[ name ][ "func" ]( *args )

def var( name ):
	'''
	Standard callback function to retrieve constants from Python's math module.
	'''

	if not name in _var_defs:
		raise exception.NoVarException( name )

	return _var_defs[ name ]
