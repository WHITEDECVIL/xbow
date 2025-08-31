import uuid

def generate(domain="oastify.com"):
    token = str(uuid.uuid4()).replace("-", "")
    callback = f"{token}.{domain}"
    print(f"[+] Generated Collaborator payload: {callback}")
    return callback

