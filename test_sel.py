# Test suite for the Selection class in MaExPa.
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

import unittest

import maexpa.selection

class SelTestCase( unittest.TestCase ):
	def test_default( self ):
		sel = maexpa.selection.Selection()
		self.assertIsNone( sel.get_var_cb() )
		self.assertIsNone( sel.get_func_cb() )

	def test_invalid( self ):
		sel = maexpa.selection.Selection()
		with self.assertRaises( Exception ):
			sel( "invalid" )

	def test_reset( self ):
		sel = maexpa.selection.Selection()
		sel( "std" )
		sel( None )
		self.assertIsNone( sel.get_var_cb() )
		self.assertIsNone( sel.get_func_cb() )

	def test_numpy( self ):
		sel = maexpa.selection.Selection()
		sel( "numpy" )
		self.assertIsNotNone( sel.get_var_cb() )
		self.assertIsNotNone( sel.get_func_cb() )

	def test_std( self ):
		sel = maexpa.selection.Selection()
		sel( "std" )
		self.assertIsNotNone( sel.get_var_cb() )
		self.assertIsNotNone( sel.get_func_cb() )

if __name__ == '__main__':
	unittest.main()
