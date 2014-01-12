# About
The conf class makes it easy to load and write data to textfiles.

# How to use

* First you need to create an instance of that class. 
* With the *addFile* method you need to specify files, which have to be loaded.
* The *loadFiles* method loads the files and parses them into the object. You can access the data over the parameter *data*

# Examples

## Load data
> conf = Conf()  
> conf.addFile("data.conf")  
> conf.loadFiles()  
> print conf.data["var"]["test"]