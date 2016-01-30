When you first load the solution into Visual Studio you need to add three paths under VC++ Directories:

1. right click the project file and select properties 
2. select VC++ Directories
3. Add the path to the bin file to Executables Directories
4. Add the path to the include file to Include Directories
5. Add the path to the lib file to Library Directories

You will additionally need to add the path to the myo32.dll:

1. Under properties again, go to Debugging
2. under Environment add PATH=yourpath;%PATH%
