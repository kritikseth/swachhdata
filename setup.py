import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swachhdata", # Replace with your own username
    version="0.1.5",
    author="Kritik Seth",
    author_email="sethkritik@gmail.com",
    description="Package that cleans your data",
    py_modules=['text'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kritikseth",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['asn1crypto', 'backports.functools-lru-cache', 'click', 'docopt', 'enum34', 'inexactsearch',
          'beautifulsoup4', 'contractions', 'regex', 'emoji', 'html2text', 'html5lib', 'MarkupSafe',
          'httplib2', 'lxml', 'nltk', 'num2words', 'pycrypto', 'textblob', 'Unidecode', 'pyahocorasick', 'pytz', 
          'unicode', 'textsearch', 'soupsieve', 'webencodings', 'pandas'
      ],
    python_requires='>=3.6'
)