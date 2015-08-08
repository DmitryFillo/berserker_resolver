import os, sys
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def dep_dnspython():
    name = 'dnspython'
    if sys.version_info[0] == 3:
        name += '3'
    return name

setup(
    name='berserker_resolver',
    version='2.0.0',
    author='Dmitry Fillo',
    author_email='fillo@fillo.me',
    maintainer_email='fillo@fillo.me',
    description=('Fast mass dns resolver which can bypass loadbalancers'),
    keywords='dns resolver berserker loadbalancer',
    license='BSD',
    url='https://github.com/DmitryFillo/berserker_resolver',
    packages=['berserker_resolver'],
    install_requires=[dep_dnspython()],
    tests_require=['mock'],
    test_suite='tests.get_suite',
    zip_safe=False,
    platforms='any',
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Internet :: Name Service (DNS)',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
