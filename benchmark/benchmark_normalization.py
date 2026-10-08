import argparse,json,time,random
ap=argparse.ArgumentParser();ap.add_argument('--records',type=int,default=10000);a=ap.parse_args()
rows=[{'id':i,'value':random.random(),'text':'sample'*4} for i in range(a.records)]
for name,fn in [('json',json.dumps),('ujson',None)]:
    if fn is None:
        try:import ujson;fn=ujson.dumps
        except ImportError:continue
    t=time.perf_counter()
    for r in rows:fn(r)
    print(f'{name}: {a.records/(time.perf_counter()-t):,.0f} records/sec')
