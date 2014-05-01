from setuptools import setup

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
        'mapping_tools',
        'test_data'
    ],
    dependency_links=[
        'git+https://github.com/natb1/mapping_tools.git#egg=mapping-tools',
        'git+https://github.com/natb1/test_data.git#egg=test-data',
    ]
)
