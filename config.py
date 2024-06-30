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
     "python-dotenv",
     "beautifulsoup4",
     "selenium",
     "psycopg2-binary"]
)