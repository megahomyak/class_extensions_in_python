# This code will raise a runtime error because of cycled import!

# What happens

Base interface imports a file with interface extension, which uses the base
interface's implementation and voila - you will get a circular dependency with
the import error!
