from setuptools import setup
import os
lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = os.path.join(lib_folder, 'requirements.txt')
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setup(name='euclinicaltrials',
    install_requires=install_requires,
    version='1.0.0',
    description='Scraping euclinicaltrials.eu, the EU\'s new Clinical Trial Information System (CTIS)',
    url='https://github.com/JulHeg/euclinicaltrials.py',
    author='Julius Hege',
    author_email='me@juliushege.com',
    license='MIT',
    packages=['euclinicaltrials'],
    zip_safe=False)