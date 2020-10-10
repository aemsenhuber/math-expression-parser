# Lexical tokens
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

import re
import operator

from . import exception

_re_int = re.compile( "[0-9]+" )
_re_float = re.compile( "([0-9]*)([.][0-9]*)?([eE][+-]?[0-9]+)?" )
_re_name = re.compile( "[a-zA-Z_][a-zA-Z_0-9]*" )

class TokenBase( object ):
	"""
	Base class for lexical tokens.
	"""

	def __init__( self, col ):
		self.col = col

	def get_column( self ):
		"""
		Get the column (or character number) of the beginning of this token.
		"""
		return self.col

	def get_type( self ):
		"""
		Get the type of this token as a str.
		"""
		raise NotImplementedError

	def get_value( self ):
		"""
		Get the
		"""
		raise NotImplementedError

class TokenName( TokenBase ):
	"""
	Token representing a variable or function reference.
	"""

	def __init__( self, col, value ):
		TokenBase.__init__( self, col )
		self.value = value

	def get_type( self ):
		return "name"

	def get_value( self ):
		return self.value

class TokenInt( TokenBase ):
	"""
	Token representing a litteral integer.
	"""

	def __init__( self, col, value ):
		TokenBase.__init__( self, col )
		self.value = value

	def get_type( self ):
		return "integer"

	def get_value( self ):
		return int( self.value )

class TokenFloat( TokenBase ):
	"""
	Token representing a litteral floating-point number.
	"""

	def __init__( self, col, value ):
		TokenBase.__init__( self, col )
		self.value = value

	def get_type( self ):
		return "float"

	def get_value( self ):
		return float( self.value )

class TokenOperator( TokenBase ):
	"""
	Token representing a mathematical operator.
	"""

	_map = {
		"**": ( operator.pow, ),
		"//": ( operator.floordiv, ),
		"*": ( operator.mul, ),
		"/": ( operator.truediv, ),
		"+": ( operator.add, operator.pos ),
		"-": ( operator.sub, operator.neg ),
	}

	def __init__( self, col, value ):
		TokenBase.__init__( self, col )
		self.value = value

	def get_type( self ):
		return "operator"

	def get_value( self ):
		return self.value

	def unary( self, value ):
		if len( self._map[ self.value ] ) == 1:
			raise Exception( "Operator {:s} is not unary".format( self.value ) )

		return self._map[ self.value ][ 1 ]( value )

	def binary( self, left, right ):
		return self._map[ self.value ][ 0 ]( left, right )

class TokenLPar( TokenBase ):
	"""
	Token representing a litteral "(".
	"""

	def get_type( self ):
		return "("

class TokenRPar( TokenBase ):
	"""
	Token representing a litteral ")".
	"""

	def get_type( self ):
		return ")"

class TokenComma( TokenBase ):
	"""
	Token representing a litteral ",".
	"""

	def get_type( self ):
		return ","

def lexer( formula ):
	"""
	Lexical analysis.
	"""

	start = 0
	tot = len( formula )

	tklist = []

	while start < tot:
		if formula[ start ] == " ":
			start += 1
			continue

		match = _re_float.match( formula, start )
		if match:
			if ( not match.group( 2 ) is None and len( match.group( 2 ) ) > 1 ) or ( len( match.group( 1 ) ) > 0 and ( not match.group( 2 ) is None or not match.group( 3 ) is None ) ):
				tklist.append( TokenFloat( start, match.group() ) )
				_, start = match.span()
				continue

		match = _re_int.match( formula, start )
		if match:
			tklist.append( TokenInt( start, match.group() ) )
			_, start = match.span()
			continue

		match = _re_name.match( formula, start )
		if match:
			tklist.append( TokenName( start, match.group() ) )
			_, start = match.span()
			continue

		for op in [ "**", "//", "*", "/", "+", "-" ]:
			if formula[ start : start+len( op ) ] == op:
				tklist.append( TokenOperator( start, op ) )
				start += len( op )
				break
		else:
			if formula[ start ] == "(":
				tklist.append( TokenLPar( start ) )
				start += 1
			elif formula[ start ] == ")":
				tklist.append( TokenRPar( start ) )
				start += 1
			elif formula[ start ] == ",":
				tklist.append( TokenComma( start ) )
				start += 1
			else:
				raise exception.LexicalException( formula[ start ], start + 1 )

	return tklist
