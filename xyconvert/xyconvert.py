"""
Created on Nov 16, 2020
@author: Can Yang

Convert xy coordinates in numpy between WGS-84, GCJ-02 and BD-09 system

xy is numpy array in shape of (N,2) with coordinates order of (lat,lon)
"""

import numpy as np

a = 6378245.0  # lngg axis
ee = 0.006693421883570923
# f = 0.00335233
# b = a * (1 - f)
# ee = (a*a - b*b)/(a*a)

def assert_xy(xy):
    np.testing.assert_equal(xy.ndim,2,"xy should be two dimension")
    np.testing.assert_equal(xy.shape[1],2,"xy should contain lng,lat only")

def __transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * np.sqrt(np.abs(lng))
    ret = ret + (20.0 * np.sin(6.0 * lng * np.pi) + 20.0 * np.sin(2.0 * lng * np.pi)) * 2.0 / 3.0
    ret = ret + (20.0 * np.sin(lat * np.pi) + 40.0 * np.sin(lat / 3.0 * np.pi)) * 2.0 / 3.0
    ret = ret + (160.0 * np.sin(lat / 12.0 * np.pi) + 320.0 * np.sin(lat * np.pi / 30.0)) * 2.0 / 3.0
    return ret

def __transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng +  0.1 * lng * lat + 0.1 * np.sqrt(abs(lng))
    ret = ret + (20.0 * np.sin(6.0 * lng * np.pi) + 20.0 * np.sin(2.0 * lng * np.pi)) * 2.0 / 3.0
    ret = ret + (20.0 * np.sin(lng * np.pi) + 40.0 * np.sin(lng / 3.0 * np.pi)) * 2.0 / 3.0
    ret = ret + (150.0 * np.sin(lng / 12.0 * np.pi) + 300.0 * np.sin(lng * np.pi / 30.0)) * 2.0 / 3.0
    return ret

def wgs2gcj(xy):
    assert_xy(xy)
    wgslng = xy[:,0]
    wgslat = xy[:,1]
    dlat = __transformlat(wgslng - 105.0, wgslat - 35.0)
    dlng = __transformlng(wgslng - 105.0, wgslat - 35.0)
    radlat = wgslat/180.0 * np.pi
    magic =  np.sin(radlat)
    magic  = 1 - ee*magic*magic
    sqrtMagic = np.sqrt(magic)
    dlat = (dlat * 180.0)/((a * (1-ee)) / (magic*sqrtMagic) * np.pi)
    dlng = (dlng * 180.0)/(a/sqrtMagic * np.cos(radlat) * np.pi)
    gcjlat = wgslat + dlat
    gcjlng = wgslng + dlng
    return np.vstack([gcjlng, gcjlat]).T

def gcj2wgs(xy):
    assert_xy(xy)
    lng = xy[:,0]
    lat = xy[:,1]
    dlat = __transformlat(lng - 105.0, lat - 35.0)
    dlng = __transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * np.pi
    magic = np.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = np.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * np.pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * np.cos(radlat) * np.pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return np.vstack([lng * 2 - mglng, lat * 2 - mglat]).T

def gcj2bd(xy):
    assert_xy(xy)
    gcjLon = xy[:,0]
    gcjLat = xy[:,1]
    z = np.sqrt(np.power(gcjLat,2) + np.power(gcjLon,2)) + 0.00002 * np.sin(gcjLat * np.pi * 3000.0/180.0)
    theta = np.arctan2(gcjLat,gcjLon) + 0.000003 * np.cos(gcjLon * np.pi * 3000.0/180.0)
    bdLon = z * np.cos(theta) + 0.0065
    bdLat = z * np.sin(theta) + 0.006
    return np.vstack([bdLon, bdLat]).T

def bd2gcj(xy):
    assert_xy(xy)
    bdLon = xy[:,0]
    bdLat = xy[:,1]
    x = bdLon - 0.0065
    y = bdLat - 0.006
    z = np.sqrt(np.power(x,2) + np.power(y,2)) - 0.00002 * np.sin(y * np.pi * 3000.0/180.0)
    theta = np.arctan2(y,x) - 0.000003 * np.cos(x * np.pi *3000.0/180.0)
    gcjLon = z * np.cos(theta)
    gcjLat = z * np.sin(theta)
    return np.vstack([gcjLon, gcjLat]).T

def wgs2bd(xy):
    assert_xy(xy)
    return gcj2bd(wgs2gcj(xy))

def bd2wgs(xy):
    assert_xy(xy)
    return gcj2wgs(bd2gcj(xy))
