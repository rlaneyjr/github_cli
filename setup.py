"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup
#from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='github_cli',
    version='0.2.2',
    description='Github CLI commands to search using Githubv3 API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rlaneyjr/github_cli',
    author='Ricky Laney',
    author_email='rlaneyjr@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='github cli commands search git repositories users',
    py_modules=['github_cli'],
    install_requires=['click', 'requests'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'gh_find=github_cli:gh_find',
            'gh_list=github_cli:gh_list',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/rlaney/github_cli/issues',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'http://saythanks.io/to/rlaneyjr',
        'Source': 'https://github.com/rlaneyjr/github_cli/',
    },
)
