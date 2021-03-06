from setuptools import setup, find_packages

setup(
    name='SinkNode',
    version='1.2.0',
    packages=find_packages(),
    url='https:\\github.com\Leenix\SinkNode',
    license='',
    author='Leenix',
    author_email='leenix48@gmail.com',
    description='General purpose ingestor for concurrent reading and writing to various endpoints',
    requires=['requests', 'netaddr','pyserial'],
    classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 4 - Beta',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
],
)
