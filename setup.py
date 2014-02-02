from distutils.core import setup

setup(
    name='py-ninja',
    version='0.1.0',
    packages=['ninja', 'ninja.nodes'],
    install_requires=[
        "requests == 0.14.1",
        "argparse==1.2.1"
    ],
)
