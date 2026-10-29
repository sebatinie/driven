def filter_rec(records): #based on condition 

    for record in records: 

        if record["active"]: 

            yield record 

 

def transform_records(records): 

    for record in records: 

        yield{ 

            "id": record["id"], 

            "value": record["field1"]*100 

        } 

 

def calculate_statistics(records): 

    
    total=0 

    count=0 

    for record in records: 

        total+=record["value"] 

        count+=1 

        return{ 

            "count": count, 

            "total": total, 

            "average": total/count if count else 0 

        } 

samples = [
    {"id": 1, "active": True, "field1": 10},
    {"id": 2, "active": False, "field1": 20},
    {"id": 3, "active": True, "field1": 30}
]


pipeline= transform_records( 

    filter_rec(samples) 

) 

stats= calculate_statistics(pipeline) 
print(stats)