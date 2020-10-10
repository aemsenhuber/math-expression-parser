import setuptools

setuptools.setup(
    name = "maexpa",
    version = "0.1",
    author = "Alexandre Emsenhuber",
    author_email = "emsenhuber@lpl.arizona.edu",
    description = "Extensible mathematical expression analyzer with callbacks for variables and functions",
    long_description = open( "README.md", "r" ).read(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/aemsenhuber/maexpa",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
