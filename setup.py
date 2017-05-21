import codecs
import setuptools

__version__ = '0.0.1'

with codecs.open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

# TODO license
setuptools.setup(
    name='mbq.metrics',
    long_description=readme,
    version=__version__,
    url='https://github.com/managedbyq/mbq.metrics',
    author='Managed by Q',
    author_email='open-source@managedbyq.com',
    maintainer='Managed by Q',
    maintainer_email='open-source@managedbyq.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
    ],
    keywords='metrics monitoring statsd',
    packages=setuptools.find_packages(),
    install_requires=[
        'datadog==0.16.0',  # pinned until 1.0.0
    ],
    zip_safe=True,
)