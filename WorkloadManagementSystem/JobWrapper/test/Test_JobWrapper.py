""" Test class for JobWrapper
"""

#pylint: disable=protected-access, missing-docstring, invalid-name, line-too-long

# imports
import unittest
import importlib
import os
import shutil

from mock import MagicMock

from DIRAC import gLogger

from DIRAC.DataManagementSystem.Client.test.mock_DM import dm_mock
from DIRAC.Resources.Catalog.test.mock_FC import fc_mock

from DIRAC.WorkloadManagementSystem.JobWrapper.JobWrapper import JobWrapper
from DIRAC.WorkloadManagementSystem.JobWrapper.WatchdogLinux import WatchdogLinux

class JobWrapperTestCase( unittest.TestCase ):
  """ Base class for the JobWrapper test cases
  """
  def setUp( self ):
    gLogger.setLevel( 'DEBUG' )

  def tearDown( self ):
    pass


class JobWrapperTestCaseSuccess( JobWrapperTestCase ):

  def test_InputData( self ):
    myJW = importlib.import_module( 'DIRAC.WorkloadManagementSystem.JobWrapper.JobWrapper' )
    myJW.getSystemSection = MagicMock()
    myJW.ModuleFactory = MagicMock()

    jw = JobWrapper()

    jw.jobArgs['InputData'] = ''
    res = jw.resolveInputData()
    self.assertFalse( res['OK'] )

    jw = JobWrapper()
    jw.jobArgs['InputData'] = 'pippo'
    jw.dm = dm_mock
    jw.fc = fc_mock
    res = jw.resolveInputData()
    self.assertTrue( res['OK'] )

    jw = JobWrapper()
    jw.jobArgs['InputData'] = 'pippo'
    jw.jobArgs['LocalSE'] = 'mySE'
    jw.jobArgs['InputDataModule'] = 'aa.bb'
    jw.dm = dm_mock
    jw.fc = fc_mock
    res = jw.resolveInputData()
    self.assertTrue( res['OK'] )

  def test__performChecks( self ):
    wd = WatchdogLinux( os.getpid(), MagicMock(), MagicMock(), 1000, 1024 * 1024 )
    res = wd._performChecks()
    self.assertTrue( res['OK'] )

  def test_execute(self):
    jw = JobWrapper()
    jw.jobArgs = {'Executable':'/bin/ls'}
    res = jw.execute('')
    self.assertTrue( res['OK'] )

    shutil.copy('WorkloadManagementSystem/JobWrapper/test/script-OK.sh', 'script-OK.sh')
    jw = JobWrapper()
    jw.jobArgs = {'Executable':'script-OK.sh'}
    res = jw.execute('')
    self.assertTrue( res['OK'] )
    os.remove('script-OK.sh')

    shutil.copy('WorkloadManagementSystem/JobWrapper/test/script.sh', 'script.sh')
    jw = JobWrapper()
    jw.jobArgs = {'Executable':'script.sh', 'Arguments':'111'}
    res = jw.execute('')
    self.assertFalse( res['OK'] )
    os.remove('script.sh')

    shutil.copy('WorkloadManagementSystem/JobWrapper/test/script-RESC.sh', 'script-RESC.sh') #this will reschedule
    jw = JobWrapper()
    jw.jobArgs = {'Executable':'script-RESC.sh'}
    res = jw.execute('')
    self.assertFalse( res['OK'] )
    os.remove('script-RESC.sh')





#############################################################################
# Test Suite run
#############################################################################

if __name__ == '__main__':
  suite = unittest.defaultTestLoader.loadTestsFromTestCase( JobWrapperTestCase )
  suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( JobWrapperTestCaseSuccess ) )
  testResult = unittest.TextTestRunner( verbosity = 2 ).run( suite )

# EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#
