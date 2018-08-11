#!/usr/bin/env python
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.

import os
import shutil
import unittest

from sos.parser import SoS_Script
from sos.targets import file_target
from sos.utils import env
# if the test is imported under sos/test, test interacive executor
if 'sos-notebook' in os.path.abspath(__file__).split(os.sep):
    from sos_notebook.workflow_executor import Interactive_Executor as Base_Executor
else:
    from sos.workflow_executor import Base_Executor


class TestActions(unittest.TestCase):
    def setUp(self):
        env.reset()
        self.temp_files = []

    def tearDown(self):
        for f in self.temp_files:
            file_target(f).unlink()

    @unittest.skipIf(not shutil.which('ruby'), 'ruby not installed')
    def testRuby(self):
        '''Test action ruby'''
        file_target('sample.txt').unlink()
        script = SoS_Script(r'''
[10]

ruby:
    fname = "sample.txt"
    somefile = File.open(fname, "w")
    somefile.puts "Hello file!"
    somefile.close

''')
        wf = script.workflow()
        Base_Executor(wf).run()
        self.assertTrue(os.path.isfile('sample.txt'))
        #
        file_target('sample.txt').unlink()


if __name__ == '__main__':
    unittest.main()
