from setuptools import setup

# TODO: with dependency_links deprecated, pip will no longer auto-install
# github requirements using setup.py one liner. instead: hack it
# (alternative: pip install -r ...)
import subprocess
github_requirements = [
    'git+https://github.com/natb1/mapping_tools.git#egg=mapping-tools',
    'git+https://github.com/natb1/test_data.git#egg=test-data'
]
for requirement in github_requirements:
    subprocess.check_call(('pip', 'install', requirement))

setup(
    name='query_tools',
    description='a collection of strategies for object persistence',
    long_description=open('README.md').read(),
    url='https://github.com/natb1/query_tools',
    author='Nathan Buesgens',
    author_email='nathan@natb1.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='development',
    packages=['query_tools'],
    install_requires=[
        'sqlalchemy', #TODO: make optional
        'mock', #TODO: make optional: only required for testing
        #'mapping-tools', #TODO: handled by github requirements
        #'test-data' #TODO: handled by github requirements
    ],
)
