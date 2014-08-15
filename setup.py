from setuptools import setup


setup(
    name='ec2-voyeur',
    version='0.0.0',
    url='https://github.com/texastribune/ec2-voyeur',
    license='BSD',
    author='Chris Chang',
    author_email='cchang@texastribune.org',
    description='List ec2 inventory',
    long_description=open('README.md').read(),
    py_modules=['voyeur'],
    entry_points={
        'console_scripts': [
            'voyeur = voyeur:main',
        ],
    },
    install_requires=[
        'boto',
        'tabulate',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
