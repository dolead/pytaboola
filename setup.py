from setuptools import setup

setup(
    name='pytaboola',
    version='0.0.2',
    packages=['pytaboola', 'pytaboola.utils', 'pytaboola.services'],
    url='https://github.com/dolead/pytaboola',
    keywords='taboola api',
    license='MIT',
    author='Antoine Français',
    author_email='antoine.francais@gmail.com',
    maintainer="Dolead",
    maintainer_email="it@dolead.com",
    description='Python client for Taboola API',
    classifiers=[
          "Programming Language :: Python :: 3",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: MIT License"],
    install_requires=['requests', 'python-dateutil']
)
