from setuptools import setup

setup(name='salesmanago_python_api',
      version='0.2',
      description='Client for Salesmanago API.',
      url='https://github.com/haloween/salesmanago-python-api',
      keywords = "salesmanago, api",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      author='Tomasz Utracki-Janeta',
      author_email='halgravity+githubrepo@gmail.com',
      license='MIT',
      zip_safe=True,
      packages=['salesmanago_python_api'],
      include_package_data=True,
      install_requires=[
          'requests'
      ]
      )