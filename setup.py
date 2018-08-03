import ast
from io import open

from setuptools import find_packages, setup

with open('kcc/version.py', 'r') as f:
    for line in f:
        if line.startswith('VERSION'):
            version = ast.literal_eval(line.strip().split('=')[-1].strip())
            break
    else:
        version = '0.0.1'

with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='kcc',
    version=version,
    description='Check kernel config for security issues',
    long_description=readme,
    author='Arjan van de Ven',
    author_email='arjan@linux.intel.com',
    url='https://github.intel.com/avandeve/kernel-config-checker',
    license='GPL-3.0',

    keywords=[
        '',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL-3.0 License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    tests_require=['pytest'],

    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'kcc = kcc.cli:cli',
        ],
    },
)
