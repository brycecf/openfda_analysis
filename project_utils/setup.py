from setuptools import setup, find_packages

setup(
    author='Bryce Freshcorn',
    author_email='bcf4kv@gmail.com',
    description='Cross-question utility package.',
    name='project_utils',
    packages=find_packages(include='project_utils'),
    version=0.1,
    dist_dir='dist',
    zip_safe=True,
    install_requires=[
        'click',
        'fire',
        'requests'
    ]
)