# Interactive prompt to interface with MaExPa.
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

from . import exception, expression

while True:
	try:
		expr = input( ">> " )
		print( expression.Expression( expr )() )
	except exception.CommonException as e:
		print( str( e ) )
	except KeyboardInterrupt:
		break
	except EOFError:
		break
