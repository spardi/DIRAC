################################################################################
# $HeadURL $
################################################################################
__RCSID__ = "$Id:  $"

from DIRAC.ResourceStatusSystem.Utilities.MySQLMonkey import MySQLMonkey
#from DIRAC.ResourceStatusSystem.Utilities.Validator   import ResourceStatusValidator

class ResourceStatusDB:
  """
  The ResourceStatusDB class is a front-end to the ResourceStatusDB MySQL db.
  It exposes four basic methods:
  
  - insert
  - update
  - get
  - delete
  
  all them defined on the MySQL monkey class.
  Moreover, there are a set of key-worded parameters that can be used, specially
  on the getX and deleteX functions ( to know more, again, check the MySQL monkey
  documentation ).
  
  The DB schema has NO foreign keys, so there may be some small consistency checks,
  called validators on the insert and update functions.  
  
  The simplest way to instantiate an object of type :class:`ResourceStatusDB`
  is simply by calling

   >>> rsDB = ResourceStatusDB()

  This way, it will use the standard :mod:`DIRAC.Core.Base.DB`.
  But there's the possibility to use other DB classes.
  For example, we could pass custom DB instantiations to it,
  provided the interface is the same exposed by :mod:`DIRAC.Core.Base.DB`.

   >>> AnotherDB = AnotherDBClass()
   >>> rsDB = ResourceStatusDB( DBin = AnotherDB )

  Alternatively, for testing purposes, you could do:

   >>> from mock import Mock
   >>> mockDB = Mock()
   >>> rsDB = ResourceStatusDB( DBin = mockDB )

  Or, if you want to work with a local DB, providing it's mySQL:

   >>> rsDB = ResourceStatusDB( DBin = [ 'UserName', 'Password' ] )
   
  The ResourceStatusDB also exposes database Schema information, either on a 
  dictionary or on a MySQLSchema tree object.
  
  - getSchema
  - inspectSchema
    
  Alternatively, we can access the MySQLSchema XML and tree as follows:
  
   >>> rsDB = ResourceStatusDB()
   >>> xml  = rsDB.mm.SCHEMA
   >>> tree = rsDB.mm.mSchema
   >>> tree
   >>> tree.GridSite
   >>> tree.GridSite.GridTier

  """ 

  def __init__( self, *args, **kwargs ):
    """Constructor."""

    if len( args ) == 1:
      if isinstance( args[ 0 ], str ):
        maxQueueSize = 10
      if isinstance( args[ 0 ], int ):
        maxQueueSize = args[ 0 ]
    elif len( args ) == 2:
      maxQueueSize = args[ 1 ]
    elif len( args ) == 0:
      maxQueueSize = 10

    if 'DBin' in kwargs.keys():
      DBin = kwargs[ 'DBin' ]
      if isinstance( DBin, list ):
        from DIRAC.Core.Utilities.MySQL import MySQL
        self.db = MySQL( 'localhost', DBin[ 0 ], DBin[ 1 ], 'ResourceStatusDB' )
      else:
        self.db = DBin
    else:
      from DIRAC.Core.Base.DB import DB
      self.db = DB( 'ResourceStatusDB', 'ResourceStatus/ResourceStatusDB', maxQueueSize )
   
    self.mm    = MySQLMonkey( self )  
    #self.rsVal = ResourceStatusValidator( self )

  def insert( self, args, kwargs ):
    """    
    Inserts args in the DB making use of kwargs where parameters such as
    the table are specified ( filled automatically by the Client). In order to 
    do the insertion, it uses MySQLMonkey to do the parsing, execution and
    error handling. Typically you will not pass kwargs to this function, unless
    you know what are you doing and you have a very special use case.    
      
    :param args: Tuple with the arguments for the delete function. Note the 
      non usage of \*args.
    :type  args: tuple
    :param kwargs: Dictionary with the keyworded arguments for the insert 
      function. Note the non usage of \*kwargs. At least, kwargs contains the 
      key table, with the table in which args are going to be inserted.
    :type kwargs: dict
    :returns: Dictionary with key Value if execution successful, otherwise key 
      Message with logs.
    :rtype: S_OK || S_ERROR
    """
    return self.mm.insert2( *args, **kwargs )

  def update( self, args, kwargs ):
    """    
    Updates row with values given on args. The row selection is done using the
    default of MySQLMonkey ( column.primary or column.keyColumn ). It can be
    modified using kwargs, but it is not explained here. The table keyword 
    argument is mandatory, and filled automatically by the Client. Typically 
    you will not pass kwargs to this function, unless you know what are you 
    doing and you have a very special use case.
       
    :param args: Tuple with the arguments for the delete function. Note the 
      non usage of \*args.
    :type  args: tuple
    :param kwargs: Dictionary with the keyworded arguments for the update 
      function. Note the non usage of \*kwargs. At least, kwargs contains the 
      key table, with the table in which args are going to be used to select 
      rows.
    :type kwargs: dict
    :returns: Dictionary with key Value if execution successful, otherwise key 
      Message with logs.
    :rtype: S_OK || S_ERROR
    """
    return self.mm.update2( *args, **kwargs )

  def get( self, args, kwargs ):
    """   
    Uses arguments to build conditional SQL statement ( WHERE ... ). If the 
    sql statement desired is more complex, you can use kwargs to interact with
    the MySQLStatement parser and generate a more sophisticated query.
       
    :param args: Tuple with the arguments for the delete function. Note the 
      non usage of \*args.
    :type  args: tuple
    :param kwargs: Dictionary with the keyworded arguments for the get 
      function. Note the non usage of \*kwargs. At least, kwargs contains the 
      key table, with the table in which args are going to be used to select 
      rows.
    :type kwargs: dict
    :returns: Dictionary with key Value if execution successful, otherwise key 
      Message with logs.
    :rtype: S_OK || S_ERROR
    """
    return self.mm.get2( *args, **kwargs )

  def delete( self, args, kwargs ):
    """     
    Uses arguments to build conditional SQL statement ( WHERE ... ). If the 
    sql statement desired is more complex, you can use kwargs to interact with
    the MySQLStatement parser and generate a more sophisticated query. There is
    only one forbidden query, with all parameters None ( this would mean a query
    of the type `DELETE * from TableName` ). The usage of kwargs is the same as in
    the get function.
      
    :param args: Tuple with the arguments for the delete function. Note the 
      non usage of \*args.
    :type  args: tuple
    :param kwargs: Dictionary with the keyworded arguments for the delete 
      function. Note the non usage of \*kwargs. At least, kwargs contains the 
      key table, with the table in which args are going to be used to select 
      rows to be deleted.
    :type kwargs: dict
    :returns: Dictionary with key Value if execution successful, otherwise key 
      Message with logs.
    :rtype: S_OK || S_ERROR
    """
    return self.mm.delete2( *args, **kwargs )
  
  def getSchema( self ):
    """      
    Returns a dictionary with database schema, this includes table and column
    names. It has two variants, columns and keyUsage. The first one has at least,
    as many keys as keyUsage, it is the complete schema. The second one is the 
    one used for the default updates and selects -- not taking into account 
    auto_increment fields, but taking into account primary and keyUsage fields.
      
    :returns: Dictionary with database schema.
    :rtype: S_OK
    """    
    return { 'OK': True, 'Value' : self.mm.SCHEMA }
    
  def inspectSchema( self ):
    """     
    Returns an object which represents the database schema and can be browsed.
     >>> db = ResourceStatusDB()
     >>> schema = db.inspectSchema()[ 'Value' ]
     >>> schema
         Schema 123:
         <TableName1>,<TableName2>...
     >>> schema.TableName1
         Table TableName1:
         <ColumnName1>,<ColumnName2>..
    
    Every column has a few attributes ( primary, keyUsage, extra, position,
    dataType and charMaxLen ). 
      
    :returns: Browsable object with schema definition.
    :rtype: S_OK
    """    
    return { 'OK': True, 'Value' : self.mm.mSchema }

      ################################################################
      #                                                              #
      #                    VALIDATION ??                             #
      #                                                              #                                       
      #  o Site             ->(IU) SiteType                          #
      #  o Service          ->(IU) ServiceType, Site                 #
      #  o Resource         ->(IU) ResourceType, ServiceType         #
      #  o StorageElement   ->(IU) Resource                          #
      #  o GridSite         ->(IU) __none__                          #
      #  o *Status          ->(IU) *,StatusType,Status               #
      #  o *ScheduledStatus ->(IU) *,StatusType,Status               #
      #  o *History         ->(IU) *,StatusType,Status               #
      ################################################################

#################################################################################
##EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF


##  '''
##  ##############################################################################
##  # MISC FUNCTIONS
##  ##############################################################################
##  '''
##  Check the booster ResourceStatusSystem.Utilities.ResourceStatusBooster
##  def setMonitoredToBeChecked( self, monitoreds, granularity, name ):
##    """
##    Set LastCheckTime to 0 to monitored(s)
##
##    :params:
##      :attr:`monitoreds`: string, or a list of strings where each is a ValidRes:
##      which granularity has to be set to be checked
##
##      :attr:`granularity`: string, a ValidRes: from who this set comes
##
##      :attr:`name`: string, name of Site or Resource
##    """
##
##    znever = datetime.min
##
##    if type( monitoreds ) is not list:
##      monitoreds = [ monitoreds ]
##
##    for monitored in monitoreds:
##
##      if monitored == 'Site':
##
##        siteName = self.getGeneralName( granularity, name, monitored )[ 'Value' ]
##        self.updateSiteStatus(siteName = siteName, lastCheckTime = znever )
##
##      elif monitored == 'Service' :
##
##        if granularity =='Site':
##          serviceName = self.getMonitoredsList( 'Service', paramsList = [ 'ServiceName' ],
##                                                siteName = name )[ 'Value' ]
##          if type( serviceName ) is not list:
##            serviceName = [ serviceName ]
##          if serviceName != []:
###            raise RSSDBException, where( self, self.setMonitoredToBeChecked ) + " No services for site %s" %name
###          else:
##            serviceName = [ x[0] for x in serviceName ]
##            self.updateServiceStatus( serviceName = serviceName, lastCheckTime = znever )
##        else:
##          serviceName = self.getGeneralName( granularity, name, monitored )[ 'Value' ]
##          self.updateServiceStatus( serviceName = serviceName, lastCheckTime = znever )
##
##      elif monitored == 'Resource':
##
##        if granularity == 'Site' :
##          resourceName = self.getMonitoredsList( 'Resource', paramsList = [ 'ResourceName' ],
##                                                 siteName = name )[ 'Value' ]
##          if type( resourceName ) is not list:
##            resourceName = [ resourceName ]
##          if resourceName != []:
##            #raise RSSDBException, where( self, self.setMonitoredToBeChecked ) + " No resources for site %s" %name
##          #else:
##            resourceName = [ x[0] for x in resourceName ]
##            self.updateResourceStatus( resourceName = resourceName, lastCheckTime = znever )
##
##        elif granularity == 'Service' :
##
##          #siteName = self.getGeneralName( granularity, name, 'Resource' )
##          serviceType, siteName = name.split('@')
##          gridSiteName          = self.getGridSiteName('Site', siteName)[ 'Value' ]
##
##          resourceName = self.getMonitoredsList( monitored, paramsList = [ 'ResourceName' ],
##                                                 gridSiteName = gridSiteName,
##                                                 serviceType = serviceType )[ 'Value' ]
##          if type( resourceName ) is not list:
##            resourceName = [ resourceName ]
##          if resourceName != []:
##         #   raise RSSDBException, where( self, self.setMonitoredToBeChecked ) + " No resources for service %s" %name
##         # else:
##            resourceName = [ x[0] for x in resourceName ]
##            self.updateResourceStatus( resourceName = resourceName, lastCheckTime = znever )
##
##        elif granularity == 'StorageElement':
##          resourceName = self.getGeneralName( granularity,  name, monitored )[ 'Value' ]
##          self.updateResourceStatus( resourceName = resourceName, lastCheckTime = znever )
##
##      # Put read and write together here... too much fomr copy/paste
##      elif monitored == 'StorageElement':
##
##        if granularity == 'Site':
##
##          gridSiteName          = self.getGridSiteName('Site', siteName)[ 'Value' ]
##          SEName = self.getMonitoredsList( monitored, paramsList = [ 'StorageElementName' ],
##                                           gridSiteName = gridSiteName )[ 'Value' ]
##          if type( SEName ) is not list:
##            SEName = [ SEName ]
##          if SEName != []:
##            #pass
##          #else:
##            SEName = [ x[0] for x in SEName ]
##            self.updateStorageElementStatus( storageElementName = SEName, lastCheckTime = znever )
##
##        elif granularity == 'Resource':
##          SEName = self.getMonitoredsList( monitored, paramsList = [ 'StorageElementName' ],
##                                           resourceName = name )[ 'Value' ]
##          if type( SEName ) is not list:
##            SEName = [ SEName ]
##          if SEName == []:
##            pass
###            raise RSSDBException, where(self, self.setMonitoredToBeChecked) + "No storage elements for resource %s" %name
##          else:
##            SEName = [ x[0] for x in SEName ]
##            self.updateStorageElementStatus( storageElementName = SEName, lastCheckTime = znever )
##
##        elif granularity == 'Service':
##
##          serviceType, siteName = name.split('@')
##          gridSiteName          = self.getGridSiteName('Site', siteName)[ 'Value' ]
##
##          SEName = self.getMonitoredsList( monitored, paramsList = [ 'StorageElementName' ],
##                                           gridSiteName = gridSiteName )[ 'Value' ]#name.split('@').pop() )[ 'Value' ]
##          if type( SEName ) is not list:
##            SEName = [ SEName ]
##          if SEName != []:
##            #pass
###            raise RSSDBException, where(self, self.setMonitoredToBeChecked) + "No storage elements for service %s" %name
##          #else:
##            SEName = [ x[0] for x in SEName ]
##            self.updateStorageElementStatus( storageElementName = SEName, lastCheckTime = znever )
################################################################################
#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF
