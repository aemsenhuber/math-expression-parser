# Test suite for "std" callbacks in MaExPa.
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

import math

import unittest

import maexpa
import maexpa.exception
import maexpa.callback_std

class StdTestCase( unittest.TestCase ):
	def test_var( self ):
		tests = [
			( "e", math.e ),
			( "pi", math.pi ),
			( "tau", math.tau ),
		]

		for expr, comp in tests:
			with self.subTest( "Constants", expr = expr ):
				res = maexpa.Expression( expr )( var = maexpa.callback_std.var )
				self.assertIs( type( res ), float )
				self.assertAlmostEqual( res, comp )

	def test_no_var( self ):
		for text in [ "xi", "lambda", "a" ]:
			with self.subTest( "Undefined constants", text = text ):
				with self.assertRaises( maexpa.exception.NoVarException ):
					maexpa.Expression( text )( var = maexpa.callback_std.var )

	def test_func_builtin_int( self ):
		tests = [
			( "min(1,2)", 1 ),
			( "max(1,2)", 2 ),
			( "min(-1,1)", -1 ),
			( "max(-1,1)", 1 ),
			( "pow(1,2)", 1 ),
			( "pow(2,3)", 8 ),
		]

		for expr, comp in tests:
			with self.subTest( "Builting functions on integers", expr = expr ):
				res = maexpa.Expression( expr )( func = maexpa.callback_std.func )
				self.assertIs( type( res ), int )
				self.assertEqual( res, comp )

	def test_func_builtin_float( self ):
		tests = [
			( "min(0.9,1.1)", 0.9 ),
			( "max(0.9,1.1)", 1.1 ),
			( "pow(2.0,4)", 16. ),
		]

		for expr, comp in tests:
			with self.subTest( "Builting functions on floats", expr = expr ):
				res = maexpa.Expression( expr )( func = maexpa.callback_std.func )
				self.assertIs( type( res ), float )
				self.assertAlmostEqual( res, comp )

	def test_func_type_float( self ):
		tests = [
			( "floor(1.7648)", 1 ),
			( "ceil(1.7648)", 2 ),
			( "floor(-1.7648)", -2 ),
			( "ceil(-1.7648)", -1 ),
		]

		for expr, comp in tests:
			with self.subTest( "Conversion from float to integer", expr = expr ):
				res = maexpa.Expression( expr )( func = maexpa.callback_std.func )
				self.assertIs( type( res ), int )
				self.assertEqual( res, comp )

	def test_func_abs_float( self ):
		tests = [
			( "abs(1.7648)", 1.7648 ),
			( "abs(-1.7648)", 1.7648 ),
		]

		for expr, comp in tests:
			with self.subTest( "Absoltue value on float", expr = expr ):
				res = maexpa.Expression( expr )( func = maexpa.callback_std.func )
				self.assertIs( type( res ), float )
				self.assertAlmostEqual( res, comp )

	def test_func_explog_float( self ):
		tests = [
			( "exp(1)", math.e ),
			( "log(e)", 1. ),
			( "log2(2)", 1. ),
			( "log10(10)", 1. ),
		]

		for expr, comp in tests:
			with self.subTest( "Exponential and logarithms on float", expr = expr ):
				res = maexpa.Expression( expr )( var = maexpa.callback_std.var, func = maexpa.callback_std.func )
				self.assertIs( type( res ), float )
				self.assertAlmostEqual( res, comp )

	def test_func_sqrt( self ):
		tests = [
			( "sqrt(2)", math.sqrt( 2. ) ),
			( "sqrt(2.)", math.sqrt( 2. ) ),
			( "sqrt(45**2)", 45. ),
		]

		for expr, comp in tests:
			with self.subTest( "Square root", expr = expr ):
				res = maexpa.Expression( expr )( var = maexpa.callback_std.var, func = maexpa.callback_std.func )
				self.assertIs( type( res ), float )
				self.assertAlmostEqual( res, comp )

	def test_func_args_num( self ):
		for text in [ "min(1)", "ceil(1,2)", "sqrt(9,16)" ]:
			with self.subTest( "Passing incorrect number of arguments", text = text ):
				with self.assertRaises( maexpa.exception.FuncArgsNumException ):
					maexpa.Expression( text )( var = maexpa.callback_std.var, func = maexpa.callback_std.func )

	def test_func_no_var( self ):
		for text in [ "e(1)", "pi(1)", "tau(1)" ]:
			with self.subTest( "Using variables as functions", text = text ):
				with self.assertRaises( maexpa.exception.NoFuncException ):
					maexpa.Expression( text )( var = maexpa.callback_std.var, func = maexpa.callback_std.func )

if __name__ == '__main__':
	unittest.main()
