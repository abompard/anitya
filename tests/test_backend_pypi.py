# -*- coding: utf-8 -*-
#
# Copyright © 2014  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2, or (at your option) any later
# version.  This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.  You
# should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# Any Red Hat trademarks that are incorporated in the source
# code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission
# of Red Hat, Inc.
#

'''
anitya tests for the pypi backend.
'''

__requires__ = ['SQLAlchemy >= 0.7']
import pkg_resources

import json
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..'))

import anitya.lib.backends.pypi as pypi
import anitya.lib.model as model
from tests import Modeltests, create_distro


class PypiBackendtests(Modeltests):
    """ pypi backend tests. """

    def setUp(self):
        """ Set up the environnment, ran before every tests. """
        super(PypiBackendtests, self).setUp()

        create_distro(self.session)
        self.create_project()

    def create_project(self):
        """ Create some basic projects to work with. """
        project = model.Project(
            name='repo_manager',
            homepage='https://pypi.python.org/pypi/repo_manager',
            backend='pypi',
        )
        self.session.add(project)
        self.session.commit()

        project = model.Project(
            name='fake',
            homepage='https://pypi.python.org/pypi/repo_manager_fake',
            backend='pypi',
        )
        self.session.add(project)
        self.session.commit()

    def test_pypi_get_version(self):
        """ Test the get_version function of the pypi backend. """
        pid = 1
        project = model.Project.get(self.session, pid)
        exp = '0.1.0'
        obs = pypi.PypiBackend.get_version(project)
        self.assertEqual(obs, exp)

        pid = 2
        project = model.Project.get(self.session, pid)
        exp = None
        obs = pypi.PypiBackend.get_version(project)
        self.assertEqual(obs, exp)

    def test_pypi_get_versions(self):
        """ Test the get_versions function of the pypi backend. """
        pid = 1
        project = model.Project.get(self.session, pid)
        exp = ['0.1.0']
        obs = pypi.PypiBackend.get_versions(project)
        self.assertEqual(obs, exp)

        pid = 2
        project = model.Project.get(self.session, pid)
        exp = None
        obs = pypi.PypiBackend.get_versions(project)
        self.assertEqual(obs, exp)


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(PypiBackendtests)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
