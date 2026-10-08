import json
class S3Archive:
    def __init__(self,bucket,client):self.bucket=bucket;self.client=client
    def archive(self,source_id,record):
        key=f"normalized/source={source_id}/{record['record_id']}.json";self.client.put_object(Bucket=self.bucket,Key=key,Body=json.dumps(record).encode());return key
class DynamoMetrics:
    def __init__(self,table):self.table=table
    def put(self,source_id,metrics):return self.table.put_item(Item={'source_id':source_id,**metrics})
class CloudWatchMetrics:
    def __init__(self,client,namespace='DataFlow'):self.client=client;self.namespace=namespace
    def put(self,source_id,metric,value,unit='Count'):return self.client.put_metric_data(Namespace=self.namespace,MetricData=[{'MetricName':metric,'Dimensions':[{'Name':'SourceId','Value':source_id}],'Value':value,'Unit':unit}])
