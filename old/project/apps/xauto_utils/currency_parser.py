###!/usr/bin/env python
###encoding:UTF-8
##
import os, re, time
from xauto.googlemap.googlemaps import GoogleMaps
gmaps = GoogleMaps('AI39si6KzAtruvWruP2-zdsMOHJwdgU3z50MwKxJRA5D5p8lNmxEeZEzA_NFwBl0ITx3POAKaYzCeYAnCvkRMNsViYsuvdyqDA')
#
#
#f = open('e:/db_curr.txt', 'r+')
##fl = open('e:/brand_new_curr.txt', 'a+')
##fr = open('e:/result.txt', 'r')
#i = 1
#for line in f:
#    ls = line.split('||')
##    n_ls = []
##    for item in ls:
##        if item:
##            n_ls.append(item)
##    cur = []
##    for i,p in enumerate(n_ls):
##        if i == 0 or i == 2 or i == 3:
##            cur.append(p.strip())
#    try:
#        lat, lng = gmaps.address_to_latlng(ls[1])
#        reverse = gmaps.reverse_geocode(lat, lng)
#        address_code = reverse['Placemark'][0]['AddressDetails']['Country']['CountryNameCode']
#        address = reverse['Placemark'][0]['AddressDetails']['Country']['CountryName']
#        print reverse['Placemark'][0]['address']
#    except Exception, e:
#        print '------------------------------>', str(e)
#        address = '>>>>>>>>>>>NOEEEEEE'
#        address_code = '__'
##    try:
##        fl.write('%s||%s||%s||%s||%s\n' % (ls[0], address_code, ls[1],  ls[2], ls[3]))
##    except Exception, e:
##        print str(e)
##        pass
#    print '%s||%s||%s||%s||%s||%s\n' % (ls[0], address, address_code, ls[1],  ls[2], ls[3])
#    time.sleep(5)
#
#f.close()

#for line in fr:
#    ls = line.split(',')
#    print '%s \t\t %s \t\t %s' % (ls[0].strip(), ls[1].strip(), ls[2].strip())
#fl.close()
#fr.close()

#fl = open('e:/event_adresses.txt', 'r')
#for line in fl:
#    print line
#    try:
#        lat, lng = gmaps.address_to_latlng(line)
#        reverse = gmaps.reverse_geocode(lat, lng)
#        address = reverse['Placemark'][0]['address']
#        print address
#    except Exception:
#        address = 'NOEEEEEE'
#
#
#fl.close()

#    f = open('e:\db_curr.txt', 'a+')
#    currencies = Currency.objects.all()
#    for curr in currencies:
#        f.write('%d||%s||%s||%s\n' % (curr.id, curr.country, curr.currency, curr.symbol))
#    f.close()

fl = open('e:/brand_new_curr.txt', 'r+')
for line in fl:
    if line.strip():
        ls = line.strip().split('||')
        print ls

fl.close()


#try:
#    lat, lng = gmaps.address_to_latlng('Honiara, Capital Territory, Solomon Islands')
#    reverse = gmaps.reverse_geocode(lat, lng)
#    address_code = reverse['Placemark'][0]['AddressDetails']['Country']['CountryNameCode']
#    address = reverse['Placemark'][0]['AddressDetails']['Country']['CountryName']
#    print reverse['Placemark'][0]['address']
#except Exception, e:
#    print '------------------------------>', str(e)
#    address = '>>>>>>>>>>>NOEEEEEE'
#    address_code = '__'
#
#print '%s||%s\n' % (address, address_code)