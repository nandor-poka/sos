#!/usr/bin/env python
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.

import os
import shutil
import subprocess
import unittest

from sos.parser import SoS_Script
from sos.targets import file_target
from sos.utils import env
# if the test is imported under sos/test, test interacive executor
if 'sos-notebook' in os.path.abspath(__file__).split(os.sep):
    from sos_notebook.workflow_executor import Interactive_Executor as Base_Executor
else:
    from sos.workflow_executor import Base_Executor


class TestTarget(unittest.TestCase):
    def setUp(self):
        env.reset()
        subprocess.call('sos remove -s', shell=True)
        self.temp_files = []

    def tearDown(self):
        for f in self.temp_files:
            file_target(f).unlink()

    @unittest.skipIf(not shutil.which('octave'), 'Octave not installed')
    def testRLibrary(self):
        '''Test target R_Library'''
        script = SoS_Script('''
[default]
depends: R_library("dplyr")
R:
    library('dplyr')
''')
        wf = script.workflow()
        Base_Executor(wf).run()

    @unittest.skipIf(not shutil.which('Rscript'), 'R not installed')
    def testDependsRLibrary(self):
        '''Testing depending on R_library'''
        # first remove xtable package
        subprocess.call('R CMD REMOVE xtable', shell=True)
        script = SoS_Script('''
[0]

depends: R_library('xtable')
R:
    library('xtable')
    ## Demonstrate data.frame
    tli.table <- xtable(cars)
''')
        wf = script.workflow()
        Base_Executor(wf).run()

    @unittest.skipIf(not shutil.which('Rscript'), 'R not installed')
    def testReexecution(self):
        '''Test re-execution of steps with R_library'''
        script = SoS_Script('''
[1]
depends: R_library("ggplot2", "2.2+")
output: '1.txt'
run: expand=True
    sleep 5
    touch {_output}
''')
        wf = script.workflow()
        Base_Executor(wf).run()
        Base_Executor(wf).run()


if __name__ == '__main__':
    unittest.main()
