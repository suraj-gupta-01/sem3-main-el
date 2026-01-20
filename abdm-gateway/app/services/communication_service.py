import uuid
from typing import Dict, List, Optional
from datetime import datetime, timezone

# In-memory storage for communication messages
_communication_messages: Dict[str, Dict] = {}
_data_requests: Dict[str, Dict] = {}
_data_responses: Dict[str, Dict] = {}


def send_message(from_bridge_id: str, to_bridge_id: str, message_type: str, payload: Dict) -> Dict:
    """Send a message from one bridge to another."""
    message_id = str(uuid.uuid4())
    _communication_messages[message_id] = {
        "id": message_id,
        "fromBridgeId": from_bridge_id,
        "toBridgeId": to_bridge_id,
        "messageType": message_type,
        "payload": payload,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "SENT"
    }
    return {"messageId": message_id, "status": "SENT"}


def request_data(hiu_id: str, hip_id: str, patient_id: str, consent_id: str,
                care_context_ids: List[str], data_types: List[str]) -> Dict:
    """Handle data request from HIU to HIP."""
    request_id = str(uuid.uuid4())
    _data_requests[request_id] = {
        "requestId": request_id,
        "hiuId": hiu_id,
        "hipId": hip_id,
        "patientId": patient_id,
        "consentId": consent_id,
        "careContextIds": care_context_ids,
        "dataTypes": data_types,
        "status": "REQUESTED",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    return {"requestId": request_id, "status": "REQUESTED"}


def respond_data(request_id: str, patient_id: str, records: List[Dict], metadata: Dict) -> Dict:
    """Handle data response from HIP to HIU."""
    if request_id not in _data_requests:
        raise ValueError("Request not found")

    _data_responses[request_id] = {
        "requestId": request_id,
        "patientId": patient_id,
        "records": records,
        "metadata": metadata,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "DELIVERED"
    }

    # Update request status
    _data_requests[request_id]["status"] = "COMPLETED"

    return {"requestId": request_id, "status": "DELIVERED"}


def get_messages_for_bridge(bridge_id: str) -> List[Dict]:
    """Get all communication messages for a specific bridge."""
    messages = []
    for message in _communication_messages.values():
        if message["fromBridgeId"] == bridge_id or message["toBridgeId"] == bridge_id:
            messages.append(message)

    # Also include data requests/responses for this bridge
    for request in _data_requests.values():
        if request["hiuId"] == bridge_id or request["hipId"] == bridge_id:
            messages.append({
                "id": request["requestId"],
                "item_type": "DATA_REQUEST",
                "fromBridgeId": request["hiuId"],
                "toBridgeId": request["hipId"],
                "timestamp": request["timestamp"],
                "status": request["status"],
                "details": request
            })

    for response in _data_responses.values():
        request = _data_requests.get(response["requestId"])
        if request and (request["hiuId"] == bridge_id or request["hipId"] == bridge_id):
            messages.append({
                "id": response["requestId"],
                "item_type": "DATA_RESPONSE",
                "fromBridgeId": request["hipId"],
                "toBridgeId": request["hiuId"],
                "timestamp": response["timestamp"],
                "status": response["status"],
                "details": response
            })

    # Sort by timestamp
    messages.sort(key=lambda x: x["timestamp"], reverse=True)
    return messages