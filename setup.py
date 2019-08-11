from os import path

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

with open(path.join(here, 'VERSION')) as f:
    version = f.read().strip()

setup(
    name='pygramtic',
    version=version,
    description='Pydantic models for Telegram Bot API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/devtul/pygramtic',
    author='devtud',
    author_email='devtud@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='pydantic telegram api bot',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.7, <4',
    install_requires=required_packages,
    project_urls={
        'Source': 'https://github.com/devtud/pygramtic',
    },
)
