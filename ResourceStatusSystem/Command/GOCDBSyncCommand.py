'''
  GOCDBSyncCommand module

  This command updates the downtime dates from the DowntimeCache table in case they changed
  after being fetched from GOCDB. In other words, it ensures that all the downtime dates in
  the database are current.

'''

import errno
import requests
import xml.dom.minidom as minidom
from DIRAC                                                      import S_OK, S_ERROR
from DIRAC.Core.LCG.GOCDBClient                                 import GOCDBClient
from DIRAC.Core.LCG.GOCDBClient                                 import _parseSingleElement
from DIRAC.ResourceStatusSystem.Command.Command                 import Command
from DIRAC.ResourceStatusSystem.Client.ResourceManagementClient import ResourceManagementClient

__RCSID__ = '$Id:  $'

class GOCDBSyncCommand( Command ):

  def __init__( self, args = None, clients = None ):

    super( GOCDBSyncCommand, self ).__init__( args, clients )

    if 'GOCDBClient' in self.apis:
      self.gClient = self.apis[ 'GOCDBClient' ]
    else:
      self.gClient = GOCDBClient()

    if 'ResourceManagementClient' in self.apis:
      self.rmClient = self.apis[ 'ResourceManagementClient' ]
    else:
      self.rmClient = ResourceManagementClient()

  def doNew( self, masterParams = None ):
    """
    Gets the downtime IDs and dates of a given hostname from the local database and compares the results
    with the remote database of GOCDB. If the downtime dates have been changed it updates the local database.

    :param: `masterParams` - string
    :return: S_OK / S_ERROR
    """

    if masterParams:
      hostname = masterParams
    else:
      return S_ERROR(errno.EINVAL, 'masterParams is not provided')

    result = self.rmClient.selectDowntimeCache( name = hostname )
    if not result[ 'OK' ]:
      return result

    for downtimes in result['Value']:

      localDBdict = { 'DowntimeID': downtimes[1],
                      'FORMATED_START_DATE': downtimes[0].strftime('%Y-%m-%d %H:%M'),
                      'FORMATED_END_DATE': downtimes[3].strftime('%Y-%m-%d %H:%M') }

      try:
        response = requests.get('https://goc.egi.eudd/gocdbpi_v4/public/?method=get_downtime&topentity=' + hostname)
        response.raise_for_status()
      except requests.exceptions.RequestException as e:
          return S_ERROR("Error %s" % e)

      doc = minidom.parseString( response.text )
      downtimeElements = doc.getElementsByTagName( "DOWNTIME" )

      for dtElement in downtimeElements:
        GOCDBdict = _parseSingleElement( dtElement, [ 'PRIMARY_KEY', 'ENDPOINT',
                                                      'FORMATED_START_DATE', 'FORMATED_END_DATE' ] )

        localDowntimeID = localDBdict['DowntimeID']
        GOCDBDowntimeID = GOCDBdict['PRIMARY_KEY'] + ' ' + GOCDBdict['ENDPOINT']

        if localDowntimeID == GOCDBDowntimeID:

          if localDBdict['FORMATED_START_DATE'] != GOCDBdict['FORMATED_START_DATE']:
            result = self.rmClient.addOrModifyDowntimeCache( downtimeID = localDBdict['DowntimeID'],
                                                        startDate = GOCDBdict['FORMATED_START_DATE'])
            if not result[ 'OK' ]:
              return result

          if localDBdict['FORMATED_END_DATE'] != GOCDBdict['FORMATED_END_DATE']:
            result = self.rmClient.addOrModifyDowntimeCache( downtimeID = localDBdict['DowntimeID'],
                                                        endDate = GOCDBdict['FORMATED_END_DATE'] )

            if not result[ 'OK' ]:
              return result

    return S_OK()

  def doCache( self ):
    return S_OK()

  def doMaster( self ):
    """
    This method calls the doNew method for each hostname that exists
    in the DowntimeCache table of the local database.

    :return: S_OK / S_ERROR
    """

    # Query DB for all downtimes
    result = self.rmClient.selectDowntimeCache( meta = { 'distinct': True } )
    if not result[ 'OK' ]:
      return result

    for data in result['Value']:

      # data[4] contains the hostname
      result = self.doNew( data[4] )
      if not result[ 'OK' ]:
        return result

    return S_OK()
