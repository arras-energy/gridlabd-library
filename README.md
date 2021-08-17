Welcome to the GridLAB-D Library

To view the current documentation, please use the [Docs Browser](http://docs.gridlabd.us/) and select the project `gridlabd-library`.

# Contributions

Libraries are stored by country, state/region, and organization, e.g., `US/CA/SLAC`.  Multiple library files may be stored in an organizations folders.  Published libraries must be listed in the folder `.index` file to be visible to the `library` subcommand.  It is also recommended that organizations add a `COPYRIGHT` and `LICENSE` file when making libraries public.

## Library Files

The format of library files must be GLM.  There are three sections in libraries.

1. Headers - This section contains library metadata.  The required meta data is as follows:

~~~
#meta library Name="<name>"
#meta library Version="<version>"
#meta library Author="<author>"
#meta library Description="<description"
#meta library Module="<modules>"
~~~

2. Requirements

Most libraries require a model, and/or class modifications.  These should be listed after the metadata and before objects.  For example, a modified `powerflow.line_configuration` class might be declared as follows:

~~~
module powerflow;
class line_configuration
{
	double line_albedo[pu];
}
~~~

3. Objects

These are the objects included in the library, e.g.,

~~~
object powerflow.line_configuration
{
	name "LC_1";
	line_albedo 0.3;
}

Note that library object names cannot begin with a numeric character. The convention is to prefix names with an acronym related to the library name.
