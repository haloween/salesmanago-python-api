import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='salesmanago_python_api',
      version='0.4',
      description='Client for Salesmanago API.',
      long_description=long_description,
      long_description_content_type="text/markdown",
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
      packages=[
          'salesmanago_python_api',
          'salesmanago_python_api.data',
          'salesmanago_python_api.services',
      ],
      include_package_data=True,
      python_requires='>=3.7',
      install_requires=[
          'requests'
      ]
      )