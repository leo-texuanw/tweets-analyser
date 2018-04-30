import ConfigParser
import urllib2
from lxml import etree
import time

config = ConfigParser.RawConfigParser()
config.read('openapi.cfg')

username=config.get('Auth', 'username')
password=config.get('Auth', 'password')

# Submit an authenticated request to the AURIN Open API
def aurin(url):

    # create an authenticated HTTP handler and submit URL
    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, url, username, password)
    auth_manager = urllib2.HTTPBasicAuthHandler(password_manager)
    opener = urllib2.build_opener(auth_manager)
    urllib2.install_opener(opener)

    req = urllib2.Request(url)
    handler = urllib2.urlopen(req)

    return handler.read()

baseurl = "http://openapi.aurin.org.au/"
url = baseurl + "wfs?service=WFS&version=2.0.0&request=DescribeFeatureType&typeName=namespace:featuretype&outputFormat=application/json"
#url = baseurl + "csw?request=GetCapabilities&service=CSW&acceptVersions=2.0.2&outputFormat=application/json"
print "SEARCH_RES:"
print aurin(url) + "123"