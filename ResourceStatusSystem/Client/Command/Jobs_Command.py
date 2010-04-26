""" The Jobs_Command class is a command class to know about 
    present jobs efficiency
"""

from DIRAC import gLogger

from DIRAC.ResourceStatusSystem.Client.Command.Command import Command
from DIRAC.ResourceStatusSystem.Utilities.Exceptions import *
from DIRAC.ResourceStatusSystem.Utilities.Utils import *

#############################################################################

class JobsStats_Command(Command):
  
  def doCommand(self, args, clientIn=None):
    """ Return getJobStats from Jobs Client  
    
       :params:
         :attr:`args`: 
           - args[0]: string: should be a ValidRes
      
           - args[1]: string: should be the name of the ValidRes
    
        returns:
          {
            'MeanProcessedJobs': X
          }
    """

    if not isinstance(args, tuple):
      raise TypeError, where(self, self.doCommand)
    
    if args[0] not in ValidRes:
      raise InvalidRes, where(self, self.doCommand)
    
    if clientIn is not None:
      c = clientIn
    else:
      from DIRAC.ResourceStatusSystem.Client.JobsClient import JobsClient   
      c = JobsClient()
      
    try:
      res = c.getJobsStats(args[0], args[1], args[2])
    except:
      gLogger.exception("Exception when calling JobsClient for %s %s" %(args[0], args[1]))
      return {'MeanProcessedJobs':'Unknown'}
    
    return {'MeanProcessedJobs':res}


#############################################################################

class JobsEff_Command(Command):
  
  def doCommand(self, args, clientIn=None):
    """ Return getJobsEff from Jobs Client  
    
       :params:
         :attr:`args`: 
           - args[0]: string: should be a ValidRes
      
           - args[1]: string: should be the name of the ValidRes
    
        returns:
          {
            'JobsEff': X
          }
    """

    if not isinstance(args, tuple):
      raise TypeError, where(self, self.doCommand)
    
    if args[0] not in ValidRes:
      raise InvalidRes, where(self, self.doCommand)
    
    if clientIn is not None:
      c = clientIn
    else:
      from DIRAC.ResourceStatusSystem.Client.JobsClient import JobsClient   
      c = JobsClient()
      
    try:
      res = c.getJobsEff(args[0], args[1], args[2])
    except:
      gLogger.exception("Exception when calling JobsClient")
      return {'JobsEff':'Unknown'}
    
    return {'JobsEff':res}


#############################################################################

class SystemCharge_Command(Command):
  
  def doCommand(self, clientIn=None):
    """ Returns last hour system charge, and the system charge of an hour before

        returns:
          {
            'LastHour': n_lastHour
            'anHourBefore': n_anHourBefore
          }
    """

    if clientIn is not None:
      c = clientIn
    else:
      from DIRAC.ResourceStatusSystem.Client.JobsClient import JobsClient   
      c = JobsClient()
      
    try:
      res = c.getSystemCharge()
    except:
      gLogger.exception("Exception when calling JobsClient")
      return {'SystemCharge':'Unknown'}
    
    return {'SystemCharge':res}

#############################################################################

class JobsEffSimple_Command(Command):
  
  def doCommand(self, args, clientIn=None):
    """ Returns simple jobs efficiency
        
       :params:
         :attr:`args`: 
           - args[0]: string: should be a ValidRes
      
           - args[1]: string should be the name of the ValidRes

        returns:
          {
            'jobsEff': 'Good'|'Fair'|'Poor'|'Idle'|'Bad'
          }
    """

    if not isinstance(args, tuple):
      raise TypeError, where(self, self.doCommand)
    
    if args[0] in ('Service', 'Services'):
      from DIRAC.ResourceStatusSystem.Client.ResourceStatusClient import ResourceStatusClient   
      c = ResourceStatusClient()
      try:
        name = c.getGeneralName(args[0], args[1], 'Site')
      except:
        gLogger.error("Can't get a general name for %s %s" %(args[0], args[1]))
        return {'JobsEff':'Unknown'}      
      granularity = 'Site'
    elif args[0] in ('Site', 'Sites'):
      name = args[1]
      granularity = args[0]
    else:
      raise InvalidRes, where(self, self.doCommand)
    
    if clientIn is not None:
      c = clientIn
    else:
      from DIRAC.ResourceStatusSystem.Client.JobsClient import JobsClient   
      c = JobsClient()
      
    try:
      res = c.getJobsSimpleEff(granularity, name)
    except:
      gLogger.exception("Exception when calling JobsClient for %s %s" %(granularity, name))
      return {'JobsEff':'Unknown'}
    
    return {'JobsEff':res}

#############################################################################
