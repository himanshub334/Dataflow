import asyncio,json,tempfile
from .connectors import FileConnector
from .pipeline import IngestionPipeline
async def main():
    with tempfile.NamedTemporaryFile(mode='w',suffix='.json',delete=False) as f:
        json.dump([{'id':1},{'id':1},{'id':2}],f);path=f.name
    p=IngestionPipeline();n=await p.ingest(FileConnector('demo',path));print({'accepted':n,'published':len(p.publisher.messages),'quarantine':len(p.quarantine)})
if __name__=='__main__':asyncio.run(main())
