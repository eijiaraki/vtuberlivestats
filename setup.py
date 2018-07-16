# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'vtuberlive',
    version      = '1.0',
    packages     = find_packages(),
    package_data = {
        'vtuberlive' : ['client_secret.json']
        },
    entry_points = {'scrapy': ['settings = vtuberlive.settings']},
)
