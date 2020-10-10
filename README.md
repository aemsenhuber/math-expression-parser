**MaExPa** (__Ma__thematical __Ex__pression __Pa__rser) is library providing a simple algebraic expression analyser, with callbacks for variable replacement and function calls, and support for implicit support of NumPy arrays.

## Aims

The goal of this library is to provide an easy way to do custom calculations on an existing dataset. If a dataset provides several fields, this library allows the end user to combine and transform fields to suit their whishes. Fields are exposed as variables in the expression, and are retrived by means of a callback function where the user-provided expression requests a mathematical variable.

## Usage

MaExPa provides on main class, `maexpa.Expression` that compiles and executes user-provided mathematical expressions. A very simple use is this:

```
import maexpa

expr = maexpa.Expression( "3*5" )
print( expr() )
```

A more complicated use case with a replacement for variables is:

```
import numpy
import maexpa

expr = maexpa.Expression( "item/total*100." )

def vars_callback( name ):
	if name == "item":
		return numpy.asarray( [ 1., 2., 3. ] )

	if name == "total":
		return numpy.asarray( [ 10., 10., 10. ] )

	raise Exception( "Unknown variable {:s}".format( name ) )

print( expr( var = vars_callback ) )
```

which will show `[10. 20. 30.]`.

## License

The library is licensed under version 2.0 of the Apache License, see the `LICENSE` file for the full terms and conditions.
