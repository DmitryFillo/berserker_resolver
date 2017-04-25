import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='berserker_resolver',
    version='3.0.0',
    author='Dmitry Fillo',
    author_email='fillo@fillo.me',
    maintainer_email='fillo@fillo.me',
    description='Fast mass dns resolver which can bypass load balancers',
    keywords='dns resolver berserker load balancers',
    license='BSD',
    url='https://github.com/DmitryFillo/berserker_resolver',
    packages=['berserker_resolver'],
    install_requires=[
        'aiodns==1.1.1',
    ],
    tests_require=[],
    test_suite='tests.suite',
    zip_safe=False,
    platforms='any',
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Internet :: Name Service (DNS)',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
