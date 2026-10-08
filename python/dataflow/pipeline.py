import hashlib,json,time,asyncio
from pydantic import BaseModel
class NormalizedRecord(BaseModel):
    source_id:str;record_id:str;payload:dict;observed_at:float;normalized_at:float
def normalize(record):
    raw=json.dumps(record.payload,sort_keys=True,separators=(',',':'))
    rid=hashlib.sha256(f'{record.source_id}:{raw}'.encode()).hexdigest()
    return NormalizedRecord(source_id=record.source_id,record_id=rid,payload=record.payload,observed_at=record.observed_at,normalized_at=time.time())
def validate(record,max_age_seconds=86400):
    if not record.payload:return False,'empty_payload'
    if record.observed_at and time.time()-record.observed_at>max_age_seconds:return False,'stale_record'
    return True,''
class InMemoryDeduplicator:
    def __init__(self):self.keys=set()
    async def setnx(self,key):
        if key in self.keys:return False
        self.keys.add(key);return True
class StreamPublisher:
    def __init__(self):self.messages=[]
    async def publish(self,record):self.messages.append(record.model_dump())
class IngestionPipeline:
    def __init__(self,dedup=None,publisher=None):self.dedup=dedup or InMemoryDeduplicator();self.publisher=publisher or StreamPublisher();self.quarantine=[]
    async def ingest(self,connector):
        accepted=0
        async for raw in connector.records():
            rec=normalize(raw);ok,reason=validate(rec)
            if not ok:self.quarantine.append({'record':rec.model_dump(),'reason':reason});continue
            if not await self.dedup.setnx(f'dataflow:{rec.source_id}:{rec.record_id}'):continue
            await self.publisher.publish(rec);accepted+=1
        return accepted
async def run_connectors(connectors,pipeline,concurrency=20):
    sem=asyncio.Semaphore(concurrency)
    async def run(c):
        async with sem:return await pipeline.ingest(c)
    return await asyncio.gather(*(run(c) for c in connectors))
