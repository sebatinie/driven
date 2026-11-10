import ijson

def filter_users_by_domain(file_path, domain_suffix):
    with open(file_path, "rb") as file:
        for user in ijson.items(file, "item"):
            email = user.get("email", "")

            if email.endswith("@" + domain_suffix):
                yield user
# def filter_users_by_domain(file_path, domain_suffix):
#     matching_users = []

#     try:
#         with open(file_path, "rb") as file:
#             for user in ijson.items(file, "item"):
#                 email = user.get("email", "")

#                 if "@" in email:
#                     domain = email.rsplit("@", 1)[1]

#                     if domain.lower().endswith(domain_suffix.lower()):
#                         matching_users.append(user)

#     except FileNotFoundError:
#         print(f"Error: File '{file_path}' not found.")

#     except ijson.JSONError as e:
#         print(f"Invalid JSON format: {e}")

#     except Exception as e:
#         print(f"Unexpected error: {e}")

#     return matching_users
if __name__ == "__main__":
    result = filter_users_by_domain(
        "users.json",
        "example.com"
    )

    for user in result:
        print(user)

# if __name__ == "__main__":
#     result = list(
#         filter_users_by_domain(
#             "users.json",
#             "example.com"
#         )
#     )

#     print(result)