from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pytaboola',
    version='0.1.3',
    packages=['pytaboola', 'pytaboola.utils', 'pytaboola.services'],
    url='https://github.com/dolead/pytaboola',
    keywords='taboola api',
    license='MIT',
    author='Antoine Francais',
    author_email='antoine.francais@gmail.com',
    maintainer="Dolead",
    maintainer_email="it@dolead.com",
    description='Python client for Taboola API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
          "Programming Language :: Python :: 3",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: MIT License"],
    install_requires=['requests', 'python-dateutil']
)
