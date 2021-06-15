from setuptools import setup


setup(
    name='Core module for vsdkx',
    url='https://gitlab.com/natix/visiondeploy/aiconnector',
    author='Helmut',
    author_email='helmut@natix.io',
    packages=['vsdkx', 'vsdkx/core'],
    install_requires=[
        'ai_connector @ git+https://gitlab+deploy-token-432901:B7knEYm-ywm6GSmjKrs9@gitlab.com/natix/visiondeploy/aiconnector.git',
        'argparse',
        'opencv-python~=4.2.0.34',
        'pyyaml',
        'numpy==1.18.5',
        'tensorflow==2.3.1',

    ],
    version='1.0',
)
