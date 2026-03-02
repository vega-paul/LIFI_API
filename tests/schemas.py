from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union

class FeeCost(BaseModel):
    name: str
    description: Optional[str] = None
    percentage: str
    token: Dict[str, Any]  # Token model
    amount: str
    amountUSD: str
    included: bool

class GasCost(BaseModel):
    type: str  # e.g., "SEND", "APPROVE"
    price: str
    estimate: str
    limit: str
    amount: str
    amountUSD: str
    token: Dict[str, Any]  # Token model

class Estimate(BaseModel):
    tool: str
    fromAmount: str
    fromAmountUSD: Optional[str] = None
    toAmount: str
    toAmountMin: str
    toAmountUSD: Optional[str] = None
    approvalAddress: str
    feeCosts: List[FeeCost]
    gasCosts: List[GasCost]
    executionDuration: int
    data: Optional[Dict[str, Any]] = None

class TransactionRequest(BaseModel):
    to: str
    data: str
    value: str
    gasLimit: str
    gasPrice: str
    chainId: int
    from_: Optional[str] = Field(None, alias="from")

class Action(BaseModel):
    fromToken: Dict[str, Any]
    fromAmount: str
    toToken: Dict[str, Any]
    fromChainId: int
    toChainId: int
    slippage: float
    fromAddress: str
    toAddress: Optional[str] = None

class ToolDetails(BaseModel):
    key: str
    name: str
    logoURI: str

class IncludedStep(BaseModel):
    id: str
    type: str
    action: Dict[str, Any]
    estimate: Estimate
    tool: str
    toolDetails: ToolDetails

class QuoteResponse(BaseModel):
    type: str
    id: str
    tool: str
    toolDetails: ToolDetails
    action: Action
    estimate: Estimate
    includedSteps: Optional[List[IncludedStep]] = None
    integrator: Optional[str] = None
    transactionRequest: TransactionRequest
    transactionId: Optional[str] = None

class RouteStep(BaseModel):
    id: str
    type: str  # "swap", "cross", "lifi", "protocol"
    tool: str
    toolDetails: Dict[str, Any]
    action: Dict[str, Any]  # Action model
    estimate: Estimate
    integrator: Optional[str] = None
    includedSteps: Optional[List[Dict[str, Any]]] = None
    referrer: Optional[str] = None

class Route(BaseModel):
    id: str
    fromChainId: int
    fromAmountUSD: str
    fromAmount: str
    fromToken: Dict[str, Any]  # Token model
    toChainId: int
    toAmountUSD: str
    toAmount: str
    toAmountMin: str
    toToken: Dict[str, Any]  # Token model
    gasCostUSD: str
    steps: List[RouteStep]
    fromAddress: Optional[str] = None
    toAddress: Optional[str] = None
    containsSwitchChain: Optional[bool] = None

class UnavailableRoutes(BaseModel):
    filteredOut: Optional[List[Dict[str, Any]]] = None
    failed: Optional[List[Dict[str, Any]]] = None

class RoutesResponse(BaseModel):
    routes: List[Route]
    unavailableRoutes: Optional[Dict[str, Any]] = None

class ChainPair(BaseModel):
    fromChainId: int
    toChainId: int

class Bridge(BaseModel):
    key: str
    name: str
    logoURI: str
    supportedChains: List[ChainPair]

class Exchange(BaseModel):
    key: str
    name: str
    logoURI: str
    supportedChains: List[int]

class ToolsResponse(BaseModel):
    bridges: List[Bridge]
    exchanges: List[Exchange]
