import os, sys
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

dnspython = 'dnspython'

if sys.version_info.major == 3:
    dnspython += '3'

setup(
    name = 'berserker_resolver',
    version = '0.0.2',
    author = 'Dmitry Fillo',
    author_email = 'fillo@fillo.me',
    description = ('Berserker Resolver is fast mass dns resolver which can bypass loadbalancers'),
    license = 'BSD',
    keywords = 'dns resolver berserker loadbalancer',
    url = 'https://github.com/DmitryFillo/berserker_resolver',
    packages=['berserker_resolver'],
    install_requires=[dnspython],
    setup_requires=[dnspython],
    zip_safe=False,
    platforms='any',
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Internet :: Name Service (DNS)',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
    ],
)
