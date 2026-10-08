import sys,asyncio,json,tempfile
sys.path.insert(0,'python')
from dataflow.pipeline import IngestionPipeline
from dataflow.connectors import FileConnector
def test_dedup():
    with tempfile.NamedTemporaryFile(mode='w',suffix='.json',delete=False) as f:json.dump([{'id':1},{'id':1},{'id':2}],f);path=f.name
    p=IngestionPipeline();assert asyncio.run(p.ingest(FileConnector('s',path)))==2
