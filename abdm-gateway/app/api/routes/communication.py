from fastapi import APIRouter, Depends, HTTPException, status
from app.deps.headers import require_gateway_headers
from app.deps.auth import get_current_token
from app.api.schemas import (
    SendMessageRequest, SendMessageResponse,
    DataRequest, DataResponse, MessageHistoryItem, MessageHistoryResponse
)
from app.services.communication_service import (
    send_message, request_data, respond_data, get_messages_for_bridge
)

router = APIRouter(prefix="/communication", tags=["communication"])


@router.post("/send-message", response_model=SendMessageResponse)
def send_message_endpoint(body: SendMessageRequest,
                         token=Depends(get_current_token),
                         headers=Depends(require_gateway_headers)):
    """Send a message from one bridge to another."""
    return SendMessageResponse(
        **send_message(body.fromBridgeId, body.toBridgeId, body.messageType, body.payload)
    )


@router.post("/data-request")
def data_request_endpoint(body: DataRequest,
                         token=Depends(get_current_token),
                         headers=Depends(require_gateway_headers)):
    """Handle data request from HIU to HIP."""
    return request_data(body.hiuId, body.hipId, body.patientId, body.consentId,
                       body.careContextIds, body.dataTypes)


@router.post("/data-response")
def data_response_endpoint(body: DataResponse,
                          token=Depends(get_current_token),
                          headers=Depends(require_gateway_headers)):
    """Handle data response from HIP to HIU."""
    try:
        return respond_data(body.requestId, body.patientId, body.records, body.metadata)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/messages/{bridge_id}", response_model=MessageHistoryResponse)
def get_messages_endpoint(bridge_id: str,
                         token=Depends(get_current_token)):
    """Get communication history for a bridge."""
    messages = get_messages_for_bridge(bridge_id)
    return {"messages": messages}