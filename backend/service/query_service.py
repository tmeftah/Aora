import json
import uuid
from fastapi.responses import StreamingResponse

from backend.rag_llms_langchain import chain
from backend.embeddings.ingest import get_vectorstore


def query_service(query: str):
    """
    Process a query and return a streaming response.
    """

    store = get_vectorstore()
    docs = store.invoke(query)

    print(20 * "*", "docs", 20 * "*", "\n", docs)

    async def stream_generator():
        print(20 * "*", "\n", query)
        async for text in chain.astream({"input": query, "context": docs}):
            yield json.dumps({"event_id": str(uuid.uuid4()), "data": text})

        # TODO  here we have to add the metadata/source

    return StreamingResponse(stream_generator(),
                             media_type="application/x-ndjson")
