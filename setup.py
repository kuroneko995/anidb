try:
    from setuptools import setup
    import py2exe
except ImportError:
    from distutils.core import setup
    
config = {
    'description': 'anidb',
    'author': 'Dang Minh Nguyen',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'ndminh92@gmail.com',
    'version': '0.9',
    'install_requires': ['nose'],
    'packages':['anidb'],
    'py_modules':[],
    'scripts':[],
    'name': 'anidb_project',
    'console':['program.py']
}

setup(**config)
