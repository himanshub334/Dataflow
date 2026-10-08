from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterator, Any
import csv, json
@dataclass
class Record:
    source_id: str; payload: dict[str,Any]; observed_at: float
class SourceConnector(ABC):
    def __init__(self,source_id): self.source_id=source_id
    @abstractmethod
    async def records(self)->AsyncIterator[Record]: yield Record('',{},0)
class RESTConnector(SourceConnector):
    def __init__(self,source_id,url,client): super().__init__(source_id);self.url=url;self.client=client
    async def records(self):
        r=await self.client.get(self.url);r.raise_for_status();data=r.json()
        for item in data if isinstance(data,list) else data.get('records',[]): yield Record(self.source_id,item,0)
class FileConnector(SourceConnector):
    def __init__(self,source_id,path): super().__init__(source_id);self.path=path
    async def records(self):
        if self.path.endswith('.csv'):
            with open(self.path,newline='',encoding='utf-8') as f:
                for row in csv.DictReader(f): yield Record(self.source_id,dict(row),0)
        else:
            with open(self.path,encoding='utf-8') as f:data=json.load(f)
            for item in data if isinstance(data,list) else [data]: yield Record(self.source_id,item,0)
class MQTTConnector(SourceConnector):
    async def records(self):
        if False: yield Record(self.source_id,{},0)
class DatabaseConnector(SourceConnector):
    async def records(self):
        if False: yield Record(self.source_id,{},0)
