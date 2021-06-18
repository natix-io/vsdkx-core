from setuptools import setup, find_namespace_packages


setup(
    name='vsdkx-core',
    url='https://gitlab.com/natix/cvison/vsdkx/vsdkx-core',
    author='Helmut',
    author_email='helmut@natix.io',
    namespace_packages=['vsdkx'],
    packages=find_namespace_packages(include=['vsdkx*']),
    install_requires=[
        'ai_connector @ git+https://gitlab+deploy-token-432901:B7knEYm-ywm6GSmjKrs9@gitlab.com/natix/visiondeploy/aiconnector.git@1.0',
        'argparse',
        'opencv-python~=4.2.0.34',
        'pyyaml',
        'numpy==1.18.5',
        'tensorflow==2.3.1',

    ],
    version='1.0',
)
