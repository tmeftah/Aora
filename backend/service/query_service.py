import json
import uuid

from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from backend.embeddings.ingest import get_vectorstore
from backend.exceptions import NoValidPermissionsException
from backend.models.sqlalchemy_models import User
from backend.rag_llms_langchain import chain
from backend.service.oauth import check_current_user_permissions


async def query_service(query: str, current_user: User, db: Session):
    """
    Process a query and return a streaming response.
    """
    user_has_permissions = check_current_user_permissions(
        current_user=current_user, db=db
    )
    if not user_has_permissions:
        raise NoValidPermissionsException()

    store = get_vectorstore()
    docs = store.invoke(query)

    print(20 * "*", "docs", 20 * "*", "\n", docs)

    async def stream_generator():
        print(20 * "*", "\n", query)
        async for text in chain.astream({"input": query, "context": docs}):
            yield json.dumps({"event_id": str(uuid.uuid4()), "data": text})

        # TODO  here we have to add the metadata/source

    return StreamingResponse(
        stream_generator(), media_type="application/x-ndjson"
    )
