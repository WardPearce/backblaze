from setuptools import setup

def get_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()

setup(
    name='aiob2',
    version='0.1.0',
    description='Asynchronous backblaze b2 wrapper.',
    author='WardPearce',
    author_email='contact@districtnine.host',
    install_requires=get_requirements(),
    license='Apache License 2.0',
    packages=['aiob2', 'aiob2.account', 'aiob2.bucket', 'aiob2.file', 'aiob2.source_file'],
    zip_safe=False
)
