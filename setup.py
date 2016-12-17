from setuptools import setup


setup(
    name='git-server',
    version='0.0.1',
    author='Nir Cohen',
    packages=[
        'gif_server',
    ],
    entry_points={
        'console_scripts': [
            'git-server = git_server.main:main',
        ]
    },
    install_requires=[
        'click>=6.6',
        'boto==2.45.0',
        'Flask==0.11.1',
        'requests=2.12.4',
        'gunicorn==19.6.0',
        'voluptuous==0.9.3',
        'Flask-RESTful==0.3.4',
        'flask-restful-swagger==0.19',
    ]
)
