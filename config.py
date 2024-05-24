from setuptools import setup 

setup(
    name="Image Search",
    version="1.0.0",
    description="""
        This program searches a string passed by the user and brin images realated with 
        the term.""",
    author="Gabriel Dias",
    libraries=
    ["resquest",
     "configparser",
     "beautifulsoup4",
     "selenium"]
)