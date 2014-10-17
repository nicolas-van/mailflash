"""
mailflash
----------

A simple library to send emails.

Please refer to the online documentation for details.

Links
`````

* `documentation <https://github.com/nicolas-van/mailflash>`_
"""
from setuptools import setup


setup(
    name='mailflash',
    version='0.2.0',
    url='https://github.com/nicolas-van/mailflash',
    license='BSD',
    author='Nicolas Vanhoren',
    author_email='nicolas.vanhoren@gmail.com',
    description='Simple library to send emails',
    long_description=__doc__,
    py_modules=[
        'mailflash'
    ],
    test_suite='nose.collector',
    zip_safe=False,
    platforms='any',
    install_requires=[
        'blinker',
    ],
    tests_require=[
        'nose',
        'blinker',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
