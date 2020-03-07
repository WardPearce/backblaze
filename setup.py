from setuptools import setup

def get_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()

setup(
    name='aiob2',
    version='0.0.9',
    description='Asynchronous backblaze b2 wrapper.',
    author='WardPearce',
    author_email='contact@districtnine.host',
    install_requires=get_requirements(),
    license='Apache License 2.0',
    packages=['aiob2'],
    zip_safe=False
)
