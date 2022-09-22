import argparse
import sys
from time import time
import multiprocessing as mp


from kafka import kafka_producer, acked
from json import dumps
import h3

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--resolution',
                    dest='resolution',
                    help="H3 resolution level to generate",
                    default=6
                   )
parser.add_argument('-t', '--topic',
                    dest='topic',
                    help="The destination kafka topic",
                    default="test"
                   )
parser.add_argument('-k', '--kafka_server',
                    dest='kafka_server',
                    help="The kafka server being used with port"
                    )

args = parser.parse_args()

maxResolution    = int(args.resolution)
topic         = str(args.topic)
kafka_server  = str(args.kafka_server)
#single threaded for first version
process_count = 1

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


def produce_events(thrd):
  global kafka_server
  global maxResolution
  producer = kafka_producer(server=kafka_server)
  h3dumpjson(producer, maxResolution)
  producer.flush()

def h3dumpjson(producer, maxResolution, resolution=0, cell=None, cells=[]):
    global topic
    if(cell == None or resolution == 0):
        resolution = 0
        cell = None
        cells=[]
        lst = sorted(h3.k_ring("8029fffffffffff", 9))
    else:
        lst = h3.h3_to_children(cell, resolution)
    for itm in lst:
        if(resolution < maxResolution):
            h3dumpjson(producer, maxResolution,resolution + 1, itm, cells + [itm])
        o =  { "cell":itm, "resolution":resolution }
        for lvl in range(0, resolution):
            o["hier_" + str(lvl)] = cells[lvl]
        o["polygon"] = poly_str(itm)
        #print(dumps(o).encode('utf-8'))
        producer.produce(topic, value=dumps(o).encode('utf-8'), callback=acked)






def mp_func( thrd, tst):
  return produce_events( thrd)

if __name__ == '__main__':
  print('Start...')
  mp.freeze_support()
  process_pool = mp.Pool(processes = process_count)
  process_pool.starmap( mp_func,  [(thrd, 'test') for thrd in range(process_count)]  )
