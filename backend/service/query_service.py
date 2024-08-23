import json
import uuid

from fastapi.responses import StreamingResponse

from backend.embeddings.ingest import get_vectorstore
from backend.service.llm_utils import create_chain


async def query_service(query: str, model_name: str):
    """
    Process a query and return a streaming response.
    """

    store = get_vectorstore()
    docs = store.invoke(query)
    chain = create_chain(model_name)

    print(20 * "*", "docs", 20 * "*", "\n", docs)

    async def stream_generator():
        print(20 * "*", "\n", query)
        async for text in chain.astream({"input": query, "context": docs}):
            yield json.dumps({"event_id": str(uuid.uuid4()), "data": text})

        # TODO  here we have to add the metadata/source

    return StreamingResponse(
        stream_generator(), media_type="application/x-ndjson"
    )
