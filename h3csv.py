#!python3
# pip install 'h3==4.0.0b1'

import h3
import sys
import csv
import io
import gzip

from json import dumps, dump

def poly_str(cel):
    #x = h3.cell_to_boundary(cel, True)
    x = h3.h3_to_geo_boundary(cel, True)
    ret = "POLYGON(("
    first = True
    for y in x:
        if(first):
            ret += str(y[0]) + " " + str(y[1])
            first = False
        else:
            ret += ", " + str(y[0]) + " " + str(y[1])
    ret += "))"
    return ret

## Use this to print for a single point
def h3printOne(lat, lng, resStart, resStop):
    #print ("POINT(",lng, lat, ")")
    header = ['CELL','RESOLUTION',
              #'POLYGON',
              'TEST']
    writer = csv.writer(sys.stdout)
    writer.writerow(header)
    for resolution in range(resStart, resStop + 1):
        #cel = h3.latlng_to_cell(lat, lng, resolution)
        cel = h3.geo_to_h3(lat, lng, resolution)
        polyjson = dumps({ "type": "Polygon", "coordinates": [h3.h3_to_geo_boundary(cel, True)]}).replace('(','[').replace(')',']')
        # polyjson = h3.h3_to_geo_boundary(cel, True)
        writer.writerow([cel, resolution,
                         #poly_str(cel),
                         polyjson])

## Use this to print Everything
def h3dumpcsvgzip(resolution):
    #tplst = sorted(h3.grid_disk("8029fffffffffff", 9))
    tplst = sorted(h3.k_ring("8029fffffffffff", 9))
    totrows = 0
    fileNum = 0
    header = ['CELL','RESOLUTION','POLYGON']

    for tp in tplst:
        #lwlst = h3.cell_to_children(tp, resolution)
        lwlst = h3.h3_to_children(tp, resolution)
        for cel in lwlst:
            if(totrows % 1000000 == 0):
                if(totrows > 0):
                    with gzip.open('h3hex-'+str(resolution) + '-'+ str(fileNum) + '.csv.gz', 'wb') as gz:
                        gz.write(buff.getvalue().encode())
                        buff.close()
                buff = io.StringIO()
                writer = csv.writer(buff)
                writer.writerow(header)
                fileNum += 1
            writer.writerow([cel, resolution, poly_str(cel)])
            totrows += 1;
            # remove break to print the entire list...  note: may not need entire planet.
        # totrows += len(lwlst)
    print("Printed " + str(totrows) + " rows.")


def h3printjson(maxResolution=6, resolution=0, cell=None, cells=[]):
    if(cell == None or resolution == 0):
        resolution = 0
        cell = None
        cells=[]
        lst = sorted(h3.k_ring("8029fffffffffff", 9))
    else:
        lst = h3.h3_to_children(cell, resolution)
    for itm in lst:
        if(resolution < maxResolution):
            h3printjson(maxResolution,resolution + 1, itm, cells + [itm])
        #print(itm, resolution, cells)
        o =  {
            "cell":itm,
            "resolution":resolution
        }
        for lvl in range(0, resolution):
            o["hier_" + str(lvl)] = cells[lvl]
        o["polygon"] = poly_str(itm)
        print(dumps(o).encode('utf-8'))



if __name__ == '__main__':
    #print(h3.versions())
    #print(h3.__dict__.keys())

    #h3dumpcsvgzip(6)
    h3printOne(40.92289, -81.082317, 6, 8)
    #h3printjson(2)

    exit()