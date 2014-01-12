# About
The conf class makes it easy to load and write data to textfiles.

# How to use

## How to make a conf file

### Definitions
* **comments**: You can add comments into your conf files. Every comment begins with # and is valid until the end of that line.
* **command**: every command begins with a variable name has a = inside a data value and ends with ;
* **variable types**:
	* string: is loaded into data["var"]  
		> stringvar = "Stringvalue";
	* integer:  is loaded into data["var"]   
		> integervar = 12;
	* float:  is loaded into data["var"]   
		> floatvar = 12.23;
	* list: is loaded into data["list"]  
		> listentries[] = "first entry";  
		> listentries[] = "second entry";
	* tuple: is loadet into data["tuple"]   
		> tuplevar() = (1,2,3);



## How to load the data

* First you need to create an instance of that class. 
* With the *addFile* method you need to specify files, which have to be loaded.
* The *loadFiles* method loads the files and parses them into the object. You can access the data over the parameter *data*

# Examples

## Load data
> conf = Conf()  
> conf.addFile("data.conf")  
> conf.loadFiles()  
> print conf.data["var"]["test"]
