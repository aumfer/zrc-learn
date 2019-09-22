from setuptools import setup

setup(name='zrc_learn',
      version='0.0.1',
      install_requires=['gym'],  # And any other dependencies foo needs
      data_files=[('',["C:\\GitHub\\aumfer\\zrc-c\\build\\libzrcgym\\Release\\libzrcgym.dll"])] # no workie
)
