from setuptools import setup

with open('README.md', 'r') as fp:
    long_description = fp.read()

setup(
  name = 'control-toolbox',
  packages = ['control'],
  version = '0.0.8', 
  license='MIT',
  description = 'Python Control System Toolbox',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Rushad Mehta',
  author_email = 'rushadmehta16@gmail.com',
  url = 'https://control-toolbox.readthedocs.io/',
  download_url = 'https://github.com/rushad7/control-toolbox/archive/v0.0.8.tar.gz',
  keywords = ['Control Systems', 'Python Control Toolbox', 'System Simulation'],
  install_requires=[
          'numpy',
          'scipy',
          'sympy',
          'matplotlib',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
