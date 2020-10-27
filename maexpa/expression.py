# Mathematical expression analyser for MaExPa.
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

from . import exception, tokens

class Expression( object ):
	def __init__( self, expr, var = None, func = None ):
		self.expr = expr
		self.tokens = tokens.lexer( expr )

		# This has to be imported as run time to prevent circular reference
		from . import lib

		self.var_cbs = []
		lib_var_cb = lib.get_var_cb()
		if not lib_var_cb is None:
			self.var_cbs.append( lib_var_cb )
		if not var is None:
			self.var_cbs.append( var )

		self.func_cbs = []
		lib_func_cb = lib.get_func_cb()
		if not lib_func_cb is None:
			self.func_cbs.append( lib_func_cb )
		if not func is None:
			self.func_cbs.append( func )

		self.cur = None
		self.value = None

	def next_val( self, s ):
		if self.cur < len( self.tokens ) and self.tokens[ self.cur ].get_type() == s:
			self.value = self.tokens[ self.cur ].get_value()
			self.cur += 1
			return True
		else:
			return False

	def next_is( self, s ):
		if self.cur < len( self.tokens ) and self.tokens[ self.cur ].get_type() == s:
			self.value = None
			self.cur += 1
			return True
		else:
			return False

	def next_must( self, s ):
		if not self.next_is( s ):
			self.error()

	def operator( self, allowed ):
		if self.cur < len( self.tokens ) and self.tokens[ self.cur ].get_type() == "operator":
			if self.tokens[ self.cur ].get_value() in allowed:
				self.value = self.tokens[ self.cur ]
				self.cur += 1
				return True
		return False

	def error( self ):
		if self.cur >= len( self.tokens ):
			raise exception.ParseEndException( None, -1 )
		else:
			raise exception.ParseException( self.tokens[ self.cur ].get_type(), self.tokens[ self.cur ].get_column() + 1 )

	def __call__( self, var = None, func = None ):
		self.cur = 0
		self.value = None

		if not var is None:
			self.var_cbs.insert( 0, var )
		if not func is None:
			self.func_cbs.insert( 0, func )

		try:
			value = self.expression()
		finally:
			if not var is None:
				self.var_cbs.pop( 0 )
			if not func is None:
				self.func_cbs.pop( 0 )

		if self.cur != len( self.tokens ):
			self.error()

		return value

	def expression( self ):
		self.operator( [ "+", "-" ] )
		oper = self.value
		value = self.term()
		if oper:
			value = oper.unary( value )

		while self.operator( [ "+", "-" ] ):
			oper = self.value
			value = oper.binary( value, self.term() )

		return value

	def term( self ):
		value = self.factor()

		while self.operator( [ "*", "/", "//" ] ):
			oper = self.value
			value = oper.binary( value, self.factor() )

		return value

	def factor( self ):
		# This one is right associative :(
		bases = [ self.base() ]
		while self.operator( [ "**" ] ):
			bases.append( self.base() )

		ret = bases[ -1 ]
		for i in range( 1, len( bases ) ):
			ret = bases[ len( bases ) - i - 1 ] ** ret

		return ret

	def base( self ):
		if self.next_val( "name" ):
			name = self.value
			if self.next_is( "(" ):
				args = [ self.expression() ]
				while self.next_is( "," ):
					args.append( self.expression() )
				self.next_must( ")" )
				return self.function( name, args )
			else:
				return self.variable( name )

		if self.next_val( "float" ):
			return self.value

		if self.next_val( "integer" ):
			return self.value

		if self.next_is( "(" ):
			value = self.expression()
			self.next_must( ")" )
			return value

		self.error()

	def function( self, name, args ):
		for cb in self.func_cbs:
			try:
				return cb( name, args )
			except exception.NoFuncException:
				continue

		raise exception.NoFuncException( name )

	def variable( self, name ):
		for cb in self.var_cbs:
			try:
				return cb( name )
			except exception.NoVarException:
				continue

		raise exception.NoVarException( name )
