"""
============================
WebServices Client API
============================

This class provides a client API for all the GeoIP2 web service's end
points. The end points are Country, City, City/ISP/Org, and Omni. Each end
point returns a different set of data about an IP address, with Country
returning the least data and Omni the most.

Each web service end point is represented by a different model class, and
these model classes in turn contain multiple record classes. The record
classes have attributes which contain data about the IP address.

If the web service does not return a particular piece of data for an IP
address, the associated attribute is not populated.

The web service may not return any information for an entire record, in which
case all of the attributes for that record class will be empty.

SSL
---

Requests to the GeoIP2 web service are always made with SSL.

"""

import geoip2
import geoip2.models
import requests
from requests.utils import default_user_agent
from .errors import GeoIP2Error, HTTPError, WebServiceError

import sys

if sys.version_info[0] == 2 or (sys.version_info[0] == 3
                                and sys.version_info[1] < 3):
    import ipaddr as ipaddress  # pylint:disable=F0401
    ipaddress.ip_address = ipaddress.IPAddress
else:
    import ipaddress  # pylint:disable=F0401


class Client(object):

    """This method creates a new client object.

    It accepts the following required arguments:

    :param user_id: Your MaxMind User ID.
    :param license_key: Your MaxMind license key.

    Go to https://www.maxmind.com/en/my_license_key to see your MaxMind
    User ID and license key.

    The following keyword arguments are also accepted:

    :param host: The hostname to make a request against. This defaults to
      "geoip.maxmind.com". In most cases, you should not need to set this
      explicitly.
    :param languages: This is list of language codes. This argument will be
      passed on to record classes to use when their name properties are
      called. The default value is ['en'].

      The order of the languages is significant. When a record class has
      multiple names (country, city, etc.), its name property will return
      the name in the first language that has one.

      Note that the only language which is always present in the GeoIP2
      data is "en". If you do not include this language, the name property
      may end up returning None even when the record has an English name.

      Currently, the valid language codes are:

      * de -- German
      * en -- English names may still include accented characters if that is
        the accepted spelling in English. In other words, English does not
        mean ASCII.
      * es -- Spanish
      * fr -- French
      * ja -- Japanese
      * pt-BR -- Brazilian Portuguese
      * ru -- Russian
      * zh-CN -- Simplified Chinese.

    """

    def __init__(self, user_id, license_key, host='geoip.maxmind.com',
                 languages=None):
        if languages is None:
            languages = ['en']
        self.languages = languages
        self.user_id = user_id
        self.license_key = license_key
        self._base_uri = 'https://%s/geoip/v2.0' % (host)

    def city(self, ip_address='me'):
        """This method calls the GeoIP2 Precision City endpoint.

        :param ip_address: IPv4 or IPv6 address as a string. If no
           address is provided, the address that the web service is
           called from will be used.

        :returns: :py:class:`geoip2.models.City` object

        """
        return self._response_for('city', geoip2.models.City, ip_address)

    def city_isp_org(self, ip_address='me'):
        """This method calls the GeoIP2 Precision City/ISP/Org endpoint.

        :param ip_address: IPv4 or IPv6 address as a string. If no
          address is provided, the address that the web service is called
          from will be used.

        :returns: :py:class:`geoip2.models.CityISPOrg` object

        """
        return self._response_for('city_isp_org', geoip2.models.CityISPOrg,
                                  ip_address)

    def country(self, ip_address='me'):
        """This method calls the GeoIP2 Country endpoint.

        :param ip_address: IPv4 or IPv6 address as a string. If no address
          is provided, the address that the web service is called from will
          be used.

        :returns: :py:class:`geoip2.models.Country` object

        """
        return self._response_for('country', geoip2.models.Country,
                                  ip_address)

    def omni(self, ip_address='me'):
        """This method calls the GeoIP2 Precision Omni endpoint.

        :param ip_address: IPv4 or IPv6 address as a string. If no address
          is provided, the address that the web service is called from will
          be used.

        :returns: :py:class:`geoip2.models.Omni` object

        """
        return self._response_for('omni', geoip2.models.Omni, ip_address)

    def _response_for(self, path, model_class, ip_address):
        if ip_address != 'me':
            ip_address = str(ipaddress.ip_address(ip_address))
        uri = '/'.join([self._base_uri, path, ip_address])
        response = requests.get(uri, auth=(self.user_id, self.license_key),
                                headers={'Accept': 'application/json',
                                         'User-Agent': self._user_agent()})
        if (response.status_code == 200):  # pylint:disable=E1103
            body = self._handle_success(response, uri)
            return model_class(body, languages=self.languages)
        else:
            self._handle_error(response, uri)

    def _user_agent(self):
        return 'GeoIP2 Python Client v%s (%s)' % (geoip2.__version__,
                                                  default_user_agent())

    def _handle_success(self, response, uri):
        try:
            return response.json()
        except ValueError as ex:
            raise GeoIP2Error('Received a 200 response for %(uri)s'
                              ' but could not decode the response as '
                              'JSON: ' % locals() +
                              ', '.join(ex.args), 200, uri)

    def _handle_error(self, response, uri):
        status = response.status_code

        if status >= 400 and status < 499:
            self._handle_4xx_status(response, status, uri)
        elif status >= 500 and status < 599:
            self._handle_5xx_status(status, uri)
        else:
            self._handle_non_200_status(status, uri)

    def _handle_4xx_status(self, response, status, uri):
        if response.content and \
                response.headers['Content-Type'].find('json') >= 0:
            try:
                body = response.json()
            except ValueError as ex:
                raise HTTPError(
                    'Received a %(status)i error for %(uri)s but it did'
                    ' not include the expected JSON body: ' % locals() +
                    ', '.join(ex.args), status, uri)
            else:
                if 'code' in body and 'error' in body:
                    raise WebServiceError(body.get('error'),
                                          body.get('code'),
                                          status, uri)
                else:
                    raise HTTPError(
                        'Response contains JSON but it does not specify '
                        'code or error keys', status, uri)
        elif response.content:
            raise HTTPError('Received a %i for %s with the following '
                            'body: %s' %
                            (status, uri, response.content),
                            status, uri)
        else:
            raise HTTPError('Received a %(status)i error for %(uri)s '
                            'with no body.' % locals(), status, uri)

    def _handle_5xx_status(self, status, uri):
        raise HTTPError('Received a server error (%(status)i) for '
                        '%(uri)s' % locals(), status, uri)

    def _handle_non_200_status(self, status, uri):
        raise HTTPError('Received a very surprising HTTP status '
                        '(%(status)i) for %(uri)s' % locals(), status,
                        uri)
"""

:copyright: (c) 2013 by MaxMind, Inc.
:license: GNU Lesser General Public License v2 or later (LGPLv2+)

"""
