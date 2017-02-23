from distutils.core import setup

setup(
    name='pydrive-cli',
    version='1.0.0',
    packages=['pydrive-cli', 'pydrive-cli/model', 'pydrive-cli/auth', 'pydrive-cli/controller', 'pydrive-cli/controller/commands', 'pydrive-cli/utility'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
    install_requires=[
          'httplib2',
          'google-api-python-client',
          'colorama'
      ]
)
