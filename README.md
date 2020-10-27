**MaExPa** (**Ma**thematical **Ex**pression **Pa**rser) is library providing a simple algebraic expression analyser, with callbacks for variable replacement and function calls, and support of NumPy arrays.

## Aims

The goal of this library is to provide an easy way to do custom calculations on an existing dataset. If a dataset provides several fields, this library allows the end user to combine and transform fields to suit their whishes. Fields are exposed as variables in the expression, and are retrived by means of a callback function where the user-provided expression requests a mathematical variable.

## Usage

MaExPa provides on main class, `maexpa.Expression` that compiles and executes user-provided mathematical expressions. A very simple use is this:

```python
import maexpa

expr = maexpa.Expression( "3*5" )
print( expr() )
```

### Variable and function replacement

Callbacks for variable and function replacements can be passed when building a `maexpa.Expression` object and when computing the result:
* A callback for replacement of variables can be provided with the `var` keyword argument. That function receives a single argument, the name of the variable to replace and should return the value of the variable. In case the callback does not recognize the variable, it should raise a `maexpa.exception.NoVarException` instance.
* A callback replacement of function calls can be provided with the `func` keyword argument. That function receives two arguments, the first being the name of the function and the second a list of the arguments. It should return the result of the function. In case the callback does not recognize the variable, it should raise a `maexpa.exception.NoFuncException` instance, and a `maexpa.exception.FuncArgsNumException` instance if the user provided an incorrect number of arguments.

An use case with replacement for variables is:

```python
import numpy
import maexpa

expr = maexpa.Expression( "item/total*100." )

def vars_callback( name ):
	if name == "item":
		return numpy.asarray( [ 1., 2., 3. ] )

	if name == "total":
		return numpy.asarray( [ 10., 10., 10. ] )

	raise maexpa.exception.NoVarException( name )

print( expr( var = vars_callback ) )
```

which will show `[10. 20. 30.]`.

### Standard constants and functions

The library provides callbacks for common mathematical functions and constants. Two implementations exist: one using Python's standard library and one using `numpy`. By default neither is enabled; to use either variant, `maxepa.lib` must be called with an argument specifying which version shall be activated: "std" for Python's standard library and "numpy" for NumPy. The following is an example using the former variant:

```python
import maexpa

maexpa.lib( "std" )

expr = maexpa.Expression( "pow(2*pi,2)" )

print( expr() )
```

## License

The library is licensed under version 2.0 of the Apache License, see the `LICENSE` file for the full terms and conditions.
