from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class SendMessageRequest(BaseModel):
    fromBridgeId: str
    toBridgeId: str
    messageType: str
    payload: Dict[str, Any]


class SendMessageResponse(BaseModel):
    messageId: str
    status: str


class DataRequest(BaseModel):
    hiuId: str
    hipId: str
    patientId: str
    consentId: str
    careContextIds: List[str]
    dataTypes: List[str]


class DataResponse(BaseModel):
    requestId: str
    patientId: str
    records: List[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]] = {}


class MessageHistoryItem(BaseModel):
    id: str
    item_type: Optional[str] = None
    fromBridgeId: str
    toBridgeId: str
    timestamp: str
    status: str
    details: Optional[Dict[str, Any]] = None
    messageType: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None


class MessageHistoryResponse(BaseModel):
    messages: List["MessageHistoryItem"]