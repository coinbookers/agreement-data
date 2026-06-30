# Search-driven contract signing system
import hashlib
import json
import uuid
import time
from datetime import datetime

class SearchContract:
    def __init__(self, user, query):
        self.user = user
        self.query = query
        self.uid = str(uuid.uuid4())
        self.results = []
        self.signature = None

    def add_result(self, result):
        self.results.append({
            "result": result,
            "time": time.time()
        })

    def serialize(self):
        return json.dumps({
            "uid": self.uid,
            "user": self.user,
            "query": self.query,
            "results": self.results
        }, sort_keys=True)

    def hash(self):
        return hashlib.sha256(self.serialize().encode()).hexdigest()

    def sign(self, key):
        base = self.hash()
        self.signature = hashlib.sha256(f"{base}:{key}".encode()).hexdigest()
        return self.signature

    def verify(self, key):
        expected = hashlib.sha256(f"{self.hash()}:{key}".encode()).hexdigest()
        return expected == self.signature

def fake_search_api(query):
    return [
        f"Result for {query} - A",
        f"Result for {query} - B",
        f"Result for {query} - C"
    ]

def run():
    contract = SearchContract("UserA", "AI compliance rules")

    results = fake_search_api(contract.query)
    for r in results:
        contract.add_result(r)

    sig = contract.sign("search_secret")

    print("Contract:", contract.uid)
    print("Signature:", sig)
    print("Valid:", contract.verify("search_secret"))

    return contract

def audit(contract):
    print("\nWeb Results:")
    for r in contract.results:
        print(r)

def summary(contract):
    print("\nQuery:", contract.query)
    print("Total results:", len(contract.results))

def main():
    c = run()
    audit(c)
    summary(c)
    print("Runtime complete")

if __name__ == "__main__":
    main()
