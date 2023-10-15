from enum import Enum
from lib.Configuration import Configuration
import requests
import urllib.parse
import os
import requests

class storageType(Enum):
  LOCAL = 1
  REMOTE = 2

class pathType(Enum):
  URL = 1
  FILESYSTEMPATH = 2
  NAME = 3
  # name should be searched in places, specific for item. music files in music storage, etc.

class dataType(Enum):
  FILE = 1
  TRACK = 2
  PLAYLIST = 3
  BLOCKLIST = 4
  ALBUM = 5
  ARTISTSTRACKS = 6
  LOCALDATABASE = 7
  

class Source():
  """Wrapper for local and remote storage items"""
  def __init__(self,path:str,storageType: storageType = storageType.LOCAL, pathType: pathType = pathType.URL,dataType:dataType = dataType.FILE):
    self.path = path
    self.storageType = storageType
    self.pathType = pathType
    pass

class Database():
  def __init__(self,storageType:storageType):
    self.storageType = storageType

  def executeQuery(self,sql:str)->dict|None:
    """As database can be either local (sqlite) or remote (MySQL,Oracle,Postgres, etc), 
    consider using non platfrom specific queries\n
    returns dict made from json or None if nothing got
    """
    match self.storageType:
      case storageType.REMOTE:
        request = Configuration.getValue("apiUrl")+"/selectMetadata.php?sql="+urllib.quote_plus(sql)
        response = requests.get(request)
        if response.status_code == 200:
          return response.json()
      case storageType.LOCAL:
        pass

class Track():
  def __init__(self,source: Source):
    # set parameters
    self.source = source

    self.artists: str
    self.genre: str
    self.album: str
    self.albumTrackNumber: int
    self.title: str
    self.duration: int
    self.year: int


class Playlist():
  tracks: list
  name: str
  def __init__(self,name:str):
    self.name = name
    pass


class Client():

  authenticationKeys = {}
  connected = False
  preferLocal = True

  def __init__(self):
    pass

  def authenticate(self,credentials: set):
    """
    credentials = (username,password)
    """
    authUrl = Configuration.getValue("apiUrl") + "/authenticate.php"
    session = requests.session()
    session.auth = credentials
    # session.post(authUrl)

    answer = session.get(authUrl)

    if answer.status_code == 200:
      self.authenticationKeys = answer.cookies
      self.connected = True
    else:
      raise(Exception("PermissionDenied"))

  def getPlaylistFromSource(self,source: Source):
    match source.storageType:
      case storageType.LOCAL:
        pass
      case storageType.REMOTE:
        pass

  async def pullRemote(self):
    pass

  async def pushRemote(self):
    pass

  async def downloadTrack(self,filename:str):
    target = Configuration.getValue("localMusicStoragePath") + "/" + filename
    url = Configuration.getValue("musicStorageUrl") + "/" + urllib.quote_plus(filename)
    answer = requests.get(url)
    if answer.status_code == 200:
      with open(target,"wb") as track:
        track.write(answer.content)