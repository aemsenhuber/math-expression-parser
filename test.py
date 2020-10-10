# Test suite for for MaExPa.
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

class MaExPaTestCase( unittest.TestCase ):
	def test_int( self ):
		for text in [ "0", "1000000", "-111111111111", "+8946654", "0777" ]:
			with self.subTest( "Integer conversion", text = text ):
				self.assertEqual( maexpa.Expression( text )(), int( text ) )

	def test_float( self ):
		for text in [ "0.", ".0", "1.1", "1e10", "-1e100", "1e+10", "+2e+20", "-3e-30", "-4e+40", "-00007e-70", "00008e+80", "0009e-90", "-.1e200", "-.1e-200", "1.8765e-111", "-8.4097e+300", "+3.1415926358979" ]:
			with self.subTest( "Float conversion", text = text ):
				self.assertEqual( maexpa.Expression( text )(), float( text ) )

	def test_inv( self ):
		for text in [ "inf", "nan", ".", ".e100" ]:
			with self.subTest( "Invalid floats", text = text ):
				with self.assertRaises( maexpa.exception.CommonException ):
					maexpa.Expression( text )()

	def test_terms_int( self ):
		tests = [
			( "-1-1", -2 ),
			( "1-1", 0 ),
			( "-1+1", 0 ),
			( "1+1", 2 ),
			( "1+1+1", 3 ),
			( "1-1-1-1", -2 ),
		]

		for expr, comp in tests:
			with self.subTest( "Integer addition and substractions", expr = expr ):
				res = maexpa.Expression( expr )()
				self.assertIs( type( res ), int )
				self.assertEqual( res, comp )

	def test_terms_float( self ):
		tests = [
			( "-1.-1", -2. ),
			( "1.-1", 0. ),
			( "-1.+1", 0. ),
			( "1+1.", 2. ),
			( "1+1+1.", 3. ),
			( "1-1.-1-1", -2. ),
			( "1.5+1.5", 3. ),
			( "1.5+1.5-3.", 0. ),
		]

		for expr, comp in tests:
			with self.subTest( "Mixed integer/float addition and substractions", expr = expr ):
				res = maexpa.Expression( expr )()
				self.assertIs( type( res ), float )
				self.assertEqual( res, comp )

	def test_mult_int( self ):
		tests = [
			( "-1*1", -1 ),
			( "1*0", 0 ),
			( "0*1", 0 ),
			( "10*20", 200 ),
			( "3*4*5", 60 ),
			( "-9*9*10", -810 ),
		]

		for expr, comp in tests:
			with self.subTest( "Integer multiplication", expr = expr ):
				res = maexpa.Expression( expr )()
				self.assertIs( type( res ), int )
				self.assertEqual( res, comp )

	def test_mult_float( self ):
		tests = [
			( "-1.*2.5", -2.5 ),
			( "110*0.01", 1.1 ),
			( "1e10*1e10", 1.e20 ),
			( "-0.4*20", -8. ),
			( "3.3*4.4*5.5", 79.86 ),
			( "-9.*9.*.1", -8.1 ),
		]

		for expr, comp in tests:
			with self.subTest( "Floating-point multiplication", expr = expr ):
				res = maexpa.Expression( expr )()
				self.assertIs( type( res ), float )
				self.assertEqual( res, comp )

	def test_div_int( self ):
		tests = [
			( "-1//1", -1 ),
			( "1//1", 1 ),
			( "0//1", 0 ),
			( "10//20", 0 ),
			( "3*4//5", 2 ),
			( "-9*9//10", -8 ),
		]

		for expr, comp in tests:
			with self.subTest( "Integer division", expr = expr ):
				res = maexpa.Expression( expr )()
				self.assertIs( type( res ), int )
				self.assertEqual( res, comp )

	def test_div_int_float( self ):
		tests = [
			( "-1/1", -1. ),
			( "1/1", 1. ),
			( "0/1", 0. ),
			( "10/20", 0.5 ),
			( "3*4/5", 2.4 ),
			( "-9*9/10", -8.1 ),
		]

		for expr, comp in tests:
			with self.subTest( "Integer division resulting in float", expr = expr ):
				res = maexpa.Expression( expr )()
				self.assertIs( type( res ), float )
				self.assertEqual( res, comp )

	def test_exp_int( self ):
		tests = [
			( "0**10", 0 ),
			( "1**20", 1 ),
			( "2**2", 4 ),
			( "2**4", 16 ),
			( "2**2**2**2", 65536 ),
			( "4**3**2", 65536*4 ),
			( "2**3**3", 65536*2048 ),
			( "-10**3", -1000 ),
		]

		for expr, comp in tests:
			with self.subTest( "Integer exponentiation", expr = expr ):
				res = maexpa.Expression( expr )()
				self.assertIs( type( res ), int )
				self.assertEqual( res, comp )

	def test_exp_float( self ):
		tests = [
			( "2.5**2", 2.5**2 ),
			( "2.3**4.5", 2.3**4.5 ),
			( "-1.1**3", -1.1**3 ),
		]

		for expr, comp in tests:
			with self.subTest( "Floating-point exponentiation", expr = expr ):
				res = maexpa.Expression( expr )()
				self.assertIs( type( res ), float )
				self.assertEqual( res, comp )

	def test_no_var( self ):
		for text in [ "1+e", "0*int", "float**2", "nan*45.", "inf/1000", "none(no)" ]:
			with self.subTest( "Reference to undefined variables", text = text ):
				with self.assertRaises( maexpa.exception.NoVarException ):
					maexpa.Expression( text )()

	def test_no_func( self ):
		for text in [ "no(0)", "yes(1)", "e(10*3)", "max(10,20)" ]:
			with self.subTest( "Calls to undefined functions", text = text ):
				with self.assertRaises( maexpa.exception.NoFuncException ):
					maexpa.Expression( text )()

	def test_vars( self ):
		def consts( name ):
			if name == "e":
				return math.e
			elif name == "pi":
				return math.pi
			elif name == "ten":
				return 10.
			else:
				raise maexpa.exception.NoVarException( name, 99 )

		tests = [
			( "e", math.e ),
			( "2*pi", 2. * math.pi ),
			( "ten", 10. ),
			( "ten*ten", 100. ),
			( "ten**2", 100. ),
			( "2**ten", 1024. ),
		]

		for expr, comp in tests:
			with self.subTest( "Constants as variables", expr = expr ):
				res = maexpa.Expression( expr )( var = consts )
				self.assertIs( type( res ), float )
				self.assertEqual( res, comp )

if __name__ == '__main__':
	unittest.main()