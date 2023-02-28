from setuptools import setup

setup(
    author='Jake Mayfield',
    author_email='',
    description='A framework to rapidly develop command line applications in Python.',
    install_requires=['prompt_toolkit, rich, tabulate'],
    package_data={'express_command_line_application_framework': ['py.typed']},
    packages=['prompt_toolkit, rich, tabulate'],
    license='MIT',
    name='express_command_line_application_framework',
    url='',
    version='0.1.0'
)
