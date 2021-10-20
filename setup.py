from setuptools import setup, find_namespace_packages


setup(
    name='vsdkx-core',
    url='https://github.com/natix-io/vsdkx-core',
    author='Helmut',
    author_email='helmut@natix.io',
    namespace_packages=['vsdkx'],
    packages=find_namespace_packages(include=['vsdkx*']),
    install_requires=[
        'vsdkx-connector @ git+https://github.com/natix-io/vsdkx-connector.git@2.1',
        'argparse',
        'opencv-python~=4.2.0.34',
        'pyyaml',
        'numpy>=1.18.5',
        'tensorflow',

    ],
    version='1.0',
)
