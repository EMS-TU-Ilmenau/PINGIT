# -*- coding: utf-8 -*-
# Copyright 2019 Christoph Wagner
#     https://www.tu-ilmenau.de/it-ems/
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''Setup script for installing PINGIT with pip'''

# import modules
import sys
import os
from setuptools import setup

# global package constants
packageName     = 'pingit'
pingitScript    = 'bin/pingit'
if sys.version_info < (3, 0):
    # python 2
    import imp
    pingit = imp.load_source('pingit', pingitScript)
elif sys.version_info < (3, 3):
    # python 3.0 and up
    from importlib.machinery import SourceFileLoader
    pingit = SourceFileLoader('pingit', pingitScript).load_module()
else:
    # python 3.3 and up
    import importlib.util
    import importlib.machinery
    loader = importlib.machinery.SourceFileLoader('pingit', pingitScript)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    pingit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pingit)

packageVersion  = pingit.__version__

if __name__ == '__main__':
    setup(
        name=packageName,
        version=packageVersion,
        description=('PINGIT batch management tool for multiple nested git ' +
                     'repositories'),
        long_description='''
        PNIGIT - PINGIT Is Not a Git Indexing Tool
        ''',
        author='Christoph Wagner, EMS Research Group TU Ilmenau',
        author_email='christoph.wagner@tu-ilmenau.de',
        url='https://ems-tu-ilmenau.github.io/PINGIT/',
        license='Apache Software License',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: Quality Assurance',
            'Topic :: Software Development :: Version Control :: Git',
            'Topic :: System :: Archiving :: Backup',
            'Topic :: System :: Archiving :: Mirroring',
            'Topic :: Utilities'
        ],
        keywords=('git repository management archive batch, utility, ' +
                  'version control, mirroring, backup, quality assurance'),
        install_requires=['arghandler>=1.2', 'gitpython>=2.1'],
        scripts=[pingitScript]
    )
