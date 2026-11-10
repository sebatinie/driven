import json


def transform_users(json_string):
    users_data = json.loads(json_string)
    result = {}

    for user in users_data:
        user_id = user['id']

        transformed_user = {
            "name": user["name"],
            "contact_email": user["email"]
        }

        result[user_id] = transformed_user

    return result


sample_json = '''
[
    {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
        "created_at": "2024-01-15T10:30:00"
    },
    {
        "id": 2,
        "name": "Bob",
        "email": "bob@example.com",
        "created_at": "2024-01-16T14:45:00"
    }
]
'''

result = transform_users(sample_json)
print(result)
