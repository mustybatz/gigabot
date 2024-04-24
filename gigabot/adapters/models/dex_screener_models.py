# file: gigabot/adapters/models/dex_screener_models.py

from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class Token:
    address: str
    name: str
    symbol: str

@dataclass
class Website:
    label: str
    url: str

@dataclass
class Social:
    type: str
    url: str

@dataclass
class Info:
    imageUrl: str
    websites: List[Website]
    socials: List[Social]

@dataclass
class Pair:
    chainId: str
    dexId: str
    url: str
    pairAddress: str
    baseToken: Token
    quoteToken: Token
    priceNative: str
    priceUsd: Optional[str]
    txns: Dict[str, Dict[str, int]]
    volume: Dict[str, float]
    priceChange: Dict[str, float]
    liquidity: Optional[Dict[str, float]]
    fdv: Optional[float]
    pairCreatedAt: Optional[int]
    info: Optional[Info]

@dataclass
class PairsResponse:
    schemaVersion: str
    pairs: List[Pair]

@dataclass
class TokensResponse:
    schemaVersion: str
    pairs: List[Pair]

@dataclass
class SearchResponse:
    schemaVersion: str
    pairs: List[Pair]
