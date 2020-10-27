# Test suite for "numpy" callbacks in MaExPa.
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

import numpy

import maexpa

class StdTestCase( unittest.TestCase ):
	def setUp( self ):
		maexpa.lib( "numpy" )

	def var_cb_int( self, name ):
		if name == "a":
			return numpy.asarray( [ 2, 3, 4 ] )
		if name == "b":
			return numpy.asarray( [ 5, 1, 2 ] )
		if name == "c":
			return numpy.asarray( [ 3, 6, 4 ] )
		if name == "tot":
			return numpy.asarray( [ 10, 10, 10 ] )
		raise maexpa.exception.NoVarException( name )

	def var_cb_float( self, name ):
		if name == "a":
			return numpy.asarray( [ 0.2, 0.3, 0.4 ] )
		if name == "b":
			return numpy.asarray( [ 0.5, 0.1, 0.2 ] )
		if name == "c":
			return numpy.asarray( [ 0.3, 0.6, 0.4 ] )
		if name == "tot":
			return numpy.asarray( [ 1., 1., 1. ] )
		raise maexpa.exception.NoVarException( name )

	def comp_array( self, res, comp ):
		self.assertEqual( res.shape, comp.shape )
		for idx in range( res.shape[ 0 ] ):
			self.assertAlmostEqual( res[ idx ], comp[ idx ] )

	def test_var( self ):
		tests = [
			( "e", math.e ),
			( "pi", math.pi ),
			( "tau", math.tau ),
		]

		for expr, comp in tests:
			with self.subTest( "Constants", expr = expr ):
				res = maexpa.Expression( expr )()
				self.assertIs( type( res ), float )
				self.assertAlmostEqual( res, comp )

	def test_ops_int( self ):
		tests = [
			( "max(a,b)", numpy.asarray( [ 5, 3, 4 ] ) ),
			( "min(a,b)", numpy.asarray( [ 2, 1, 2 ] ) ),
			( "pow(tot,2)", numpy.asarray( [ 100, 100, 100 ] ) )
		]

		for expr, comp in tests:
			with self.subTest( "NumPy comparison on integers", expr = expr ):
				res = maexpa.Expression( expr )( var = self.var_cb_int )
				self.comp_array( res, comp )

	def test_ops_float( self ):
		tests = [
			( "max(a,b)", numpy.asarray( [ 0.5, 0.3, 0.4 ] ) ),
			( "min(a,b)", numpy.asarray( [ 0.2, 0.1, 0.2 ] ) ),
			( "pow(tot,2)", numpy.asarray( [ 1., 1., 1. ] ) ),
		]

		for expr, comp in tests:
			with self.subTest( "NumPy comparison on floats", expr = expr ):
				res = maexpa.Expression( expr )( var = self.var_cb_float )
				self.comp_array( res, comp )

	def test_func_mod_float( self ):
		tests = [
			( "abs(-a)", numpy.asarray( [ 0.2, 0.3, 0.4 ] ) ),
			( "floor(b)", numpy.asarray( [ 0., 0., 0. ] ) ),
			( "ceil(c)", numpy.asarray( [ 1., 1., 1. ] ) ),
		]

		for expr, comp in tests:
			with self.subTest( "Modifiers on floats", expr = expr ):
				res = maexpa.Expression( expr )( var = self.var_cb_float )
				self.comp_array( res, comp )

	def test_func_exp_int( self ):
		tests = [
			( "exp(a)", numpy.exp( numpy.asarray( [ 2., 3., 4. ] ) ) ),
			( "exp(b*c)", numpy.exp( numpy.asarray( [ 15., 6., 8. ] ) ) ),
		]

		for expr, comp in tests:
			with self.subTest( "exp on integer", expr = expr ):
				res = maexpa.Expression( expr )( var = self.var_cb_int )
				self.comp_array( res, comp )

	def test_func_exp_float( self ):
		tests = [
			( "exp(a)", numpy.exp( numpy.asarray( [ 0.2, 0.3, 0.4 ] ) ) ),
			( "exp(b*c)", numpy.exp( numpy.asarray( [ 0.15, 0.06, 0.08 ] ) ) ),
		]

		for expr, comp in tests:
			with self.subTest( "exp on floats", expr = expr ):
				res = maexpa.Expression( expr )( var = self.var_cb_float )
				self.comp_array( res, comp )

	def test_func_log_int( self ):
		tests = [
			( "log(a)", numpy.log( numpy.asarray( [ 2., 3., 4. ] ) ) ),
			( "log(b*c)", numpy.log( numpy.asarray( [ 15., 6., 8. ] ) ) ),
		]

		for expr, comp in tests:
			with self.subTest( "log on integer", expr = expr ):
				res = maexpa.Expression( expr )( var = self.var_cb_int )
				self.comp_array( res, comp )

	def test_func_log_float( self ):
		tests = [
			( "log(a)", numpy.log( numpy.asarray( [ 0.2, 0.3, 0.4 ] ) ) ),
			( "log(b*c)", numpy.log( numpy.asarray( [ 0.15, 0.06, 0.08 ] ) ) ),
		]

		for expr, comp in tests:
			with self.subTest( "log on floats", expr = expr ):
				res = maexpa.Expression( expr )( var = self.var_cb_float )
				self.comp_array( res, comp )

	def test_func_log2_int( self ):
		tests = [
			( "log2(a)", numpy.log2( numpy.asarray( [ 2., 3., 4. ] ) ) ),
			( "log2(b*c)", numpy.log2( numpy.asarray( [ 15., 6., 8. ] ) ) ),
		]

		for expr, comp in tests:
			with self.subTest( "log2 on integer", expr = expr ):
				res = maexpa.Expression( expr )( var = self.var_cb_int )
				self.comp_array( res, comp )

	def test_func_log2_float( self ):
		tests = [
			( "log2(a)", numpy.log2( numpy.asarray( [ 0.2, 0.3, 0.4 ] ) ) ),
			( "log2(b*c)", numpy.log2( numpy.asarray( [ 0.15, 0.06, 0.08 ] ) ) ),
		]

		for expr, comp in tests:
			with self.subTest( "log2 on floats", expr = expr ):
				res = maexpa.Expression( expr )( var = self.var_cb_float )
				self.comp_array( res, comp )

	def test_func_log10_int( self ):
		tests = [
			( "log10(a)", numpy.log10( numpy.asarray( [ 2., 3., 4. ] ) ) ),
			( "log10(b*c)", numpy.log10( numpy.asarray( [ 15., 6., 8. ] ) ) ),
		]

		for expr, comp in tests:
			with self.subTest( "log10 on integer", expr = expr ):
				res = maexpa.Expression( expr )( var = self.var_cb_int )
				self.comp_array( res, comp )

	def test_func_log10_float( self ):
		tests = [
			( "log10(a)", numpy.log10( numpy.asarray( [ 0.2, 0.3, 0.4 ] ) ) ),
			( "log10(b*c)", numpy.log10( numpy.asarray( [ 0.15, 0.06, 0.08 ] ) ) ),
		]

		for expr, comp in tests:
			with self.subTest( "log10 on floats", expr = expr ):
				res = maexpa.Expression( expr )( var = self.var_cb_float )
				self.comp_array( res, comp )

	def test_func_sqrt_int( self ):
		tests = [
			( "sqrt(a)", numpy.sqrt( numpy.asarray( [ 2., 3., 4. ] ) ) ),
			( "sqrt(b*c)", numpy.sqrt( numpy.asarray( [ 15., 6., 8. ] ) ) ),
		]

		for expr, comp in tests:
			with self.subTest( "Square root on integer", expr = expr ):
				res = maexpa.Expression( expr )( var = self.var_cb_int )
				self.comp_array( res, comp )

	def test_func_sqrt_float( self ):
		tests = [
			( "sqrt(a)", numpy.sqrt( numpy.asarray( [ 0.2, 0.3, 0.4 ] ) ) ),
			( "sqrt(b*c)", numpy.sqrt( numpy.asarray( [ 0.15, 0.06, 0.08 ] ) ) ),
		]

		for expr, comp in tests:
			with self.subTest( "Square root on floats", expr = expr ):
				res = maexpa.Expression( expr )( var = self.var_cb_float )
				self.comp_array( res, comp )

	def test_func_cbrt_int( self ):
		tests = [
			( "cbrt(a)", numpy.cbrt( numpy.asarray( [ 2., 3., 4. ] ) ) ),
			( "cbrt(b*c)", numpy.cbrt( numpy.asarray( [ 15., 6., 8. ] ) ) ),
		]

		for expr, comp in tests:
			with self.subTest( "Cube root on integer", expr = expr ):
				res = maexpa.Expression( expr )( var = self.var_cb_int )
				self.comp_array( res, comp )

	def test_func_cbrt_float( self ):
		tests = [
			( "cbrt(a)", numpy.cbrt( numpy.asarray( [ 0.2, 0.3, 0.4 ] ) ) ),
			( "cbrt(b*c)", numpy.cbrt( numpy.asarray( [ 0.15, 0.06, 0.08 ] ) ) ),
		]

		for expr, comp in tests:
			with self.subTest( "Cube root on floats", expr = expr ):
				res = maexpa.Expression( expr )( var = self.var_cb_float )
				self.comp_array( res, comp )
