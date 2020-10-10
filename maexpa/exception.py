# Exceptions for MaExPa.
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

class CommonException( Exception ):
	def __init__( self, desc, column ):
		self.desc = desc
		self.column = column

	def __str__( self ):
		return "{:s} at column {:d}".format( self.desc, self.column )

class LexicalException( CommonException ):
	def __str__( self ):
		return "Parse Error: unexpected character `{:s}' at column {:d}".format( self.desc, self.column )

class ParseException( CommonException ):
	def __str__( self ):
		return "Parse Error: unexpected symbol `{:s}' at column {:d}".format( self.desc, self.column )

class ParseEndException( CommonException ):
	def __str__( self ):
		return "Parse Error: unexpected end"

class NoVarException( CommonException ):
	def __str__( self ):
		return "Runtime Error: variable `{:s}' does not exist".format( self.desc )

class NoFuncException( CommonException ):
	def __str__( self ):
		return "Runtime Error: function `{:s}' does not exist".format( self.desc )
