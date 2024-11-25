## Description

This module provide some miscellaneous functions for python.

## Configuration

**/!\\** In order to use it, you have to create a local configuration file that you will not push : **import_list.py**  
This file allows you to choose which functions of this module you want to import for you project.  

If you want to import all, copy this in **import_list.py** :  
```
IMPORT_LIST = ["DevException", "UserException", "error", "check", "collection", "exec", "log", "timeout", "round", "binary", "image"]
```
Remove all modules you don't need in this list.

## Usage

This module must be used from the outside of himself.  
To use it, you have to add the containing directory of this one to your PYTHON_PATH.  
Then you have to import the module in the file where the function is needed :  
```
import xpt_utils
```
And use the function in your code : 
```
xpt_utils.function(...)
```