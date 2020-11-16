from setuptools import setup

setup(
    name='xyconvert',
    version='0.1.0',
    packages=['xyconvert'],
    license='MIT',
    description='Convert xy coordinates',
    long_description=open('README.md').read(),
	long_description_content_type="text/markdown",
    install_requires=['numpy'],
    url='https://github.com/cyang-kth/xyconvert',
    author='Can Yang',
    author_email='ycycy1990@hotmail.com'
)
