# autoprogram

# PROJECT SIDE
After creating new tool families in the project, they must be added to several modules, for example, to create the tool family "drill/drill/ic":

- the family_address variable in the Tool class in the "autoprogram\tools\drills\drills\ic.py" module must be named "drill/drill/ic"
- add "from .ic import Tool" in the "autoprogram\tools\drills\drills\__init__.py" module
- add "tools.drills.drills.ic.Tool" class in the for loop in the run method in the InitializingPage class

# FILE SYSTEM SIDE
After creating new tool families in the project, the relative path from the master programs base directory to the family directory must correspond to the path specified in the project structure.
E.g.:
tools.drills.drills.ic (project) -> autoprogram\tools\drills\drills\ic (file system)