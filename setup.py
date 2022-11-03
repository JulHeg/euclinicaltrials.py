from setuptools import setup
import os
lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + '/requirements.txt'
install_requires = [] # Here we'll get: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setup(name='euclinicaltrials',
    install_requires=install_requires,
    version='0.0.1',
    description='Scrape the euclinicaltrials.eu website',
    url='https://github.com/JulHeg/euclinicaltrials.py',
    author='Julius Hegel',
    author_email='me@juliushege.com',
    license='MIT',
    packages=['euclinicaltrials'],
    zip_safe=False)