#======================== patching qdrant_client library module to handle multi-threading issue.
import qdrant_client
import sqlite3
import wrapt
@wrapt.patch_function_wrapper(qdrant_client.local.persistence.CollectionPersistence, '__init__')
def new_init(wrapped, instance, args, kwargs):
    # here, wrapped is the original __init__,
    # instance is `self` instance (it is not true for classmethods though),
    # args and kwargs are tuple and dict respectively.

    # first call original init
    wrapped(*args, **kwargs)  # note it is already bound to the instance
    # and now do our changes
    instance.storage = sqlite3.connect(str(instance.location), check_same_thread=False)
    instance._ensure_table()
#======================== patching end.

from qdrant_client import models, QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct


client = QdrantClient(path="./vector_db")  # Persists changes to disk, fast prototyping


def recreate_collection(collection_name: str = "my_collection"):
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

def upsert(documents: list[str]: None, collection_name: str = "my_collection"):
    vectors = np.random.rand(100, 384)
    client.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                id=idx,
                vector=vector.tolist(),
                payload={"color": "red", "rand_number": idx % 10}
            )
            for idx, vector in enumerate(vectors)
        ]
    )

def search(query: str, collection_name: str = "my_collection"):
    query_vector = np.random.rand(384)
    hits = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=5  # Return 5 closest points
    )
    
    return hits