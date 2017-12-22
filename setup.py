from setuptools import setup

setup(name='jwt_auth',
      version='0.2.2',
      description='The JWT AUTH API',
      url='https://github.com/CoinLQ/jwt_auth',
      author='Xiandian',
      author_email='lvpython@gmail.com',
      license='MIT',
      packages=['jwt_auth'],
      install_requires=[
            'djangorestframework-jwt==1.11.0',
            'djangorestframework==3.6.3'
      ],
      zip_safe=False)