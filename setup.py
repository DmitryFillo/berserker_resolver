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
    name = 'berserker_resolver',
    version = '1.0.3',
    author = 'Dmitry Fillo',
    author_email = 'fillo@fillo.me',
    description = ('Berserker Resolver is fast mass dns resolver which can bypass loadbalancers'),
    license = 'BSD',
    keywords = 'dns resolver berserker loadbalancer',
    url = 'https://github.com/DmitryFillo/berserker_resolver',
    packages=['berserker_resolver'],
    install_requires=[dep_dnspython()],
    tests_require=['mock'],
    test_suite='tests.get_suite',
    zip_safe=False,
    platforms='any',
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Internet :: Name Service (DNS)',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
    ],
)
