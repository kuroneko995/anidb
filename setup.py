try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
config = {
    'description': 'anidb project',
    'author': 'Dang Minh Nguyen',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'ndminh92@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages':['anidb'],
    'py_modules':[],
    'scripts':[],
    'name': 'anidb_project'
}

setup(**config)