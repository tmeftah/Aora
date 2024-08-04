from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from backend.rag_llms_langchain import chain
from backend.embeddings.ingest import get_vectorstore

import json
import uuid


query_router = APIRouter()


@query_router.get("/query")
async def query(query: str):
    # if current_user.role < 5:
    #     raise HTTPException(status_code=403,
    # detail="Only admin users can delete other users")
    store = get_vectorstore()
    docs = store.invoke(query)

    print(20 * "*", "docs", 20 * "*", "\n", docs)

    async def stream_generator():
        # Use the LangChain model to generate text
        print(20 * "*", "\n", query)
        async for text in chain.astream({"input": query, "context": docs}):
            yield json.dumps({"event_id": str(uuid.uuid4()), "data": text})

        # TODO  here we have to add the metadata/source

    return StreamingResponse(stream_generator(), 
                            media_type="application/x-ndjson")
