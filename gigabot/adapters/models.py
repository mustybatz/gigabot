from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Tag:
    slug: str
    name: str
    category: str

@dataclass
class Platform:
    id: int
    name: str
    symbol: str
    slug: str
    token_address: str

@dataclass
class QuoteDetail:
    price: float
    volume_24h: float
    volume_change_24h: float
    percent_change_1h: float
    percent_change_24h: float
    percent_change_7d: float
    percent_change_30d: float
    percent_change_60d: float
    percent_change_90d: float
    market_cap: float
    market_cap_dominance: float
    fully_diluted_market_cap: float
    tvl: Optional[float]
    last_updated: str

@dataclass
class Quote:
    USD: QuoteDetail

@dataclass
class CryptocurrencyQuote:
    id: int
    name: str
    symbol: str
    slug: str
    num_market_pairs: int
    date_added: str
    tags: List[Tag]
    max_supply: int
    circulating_supply: int
    total_supply: int
    platform: Platform
    is_active: int
    infinite_supply: bool
    cmc_rank: int
    is_fiat: int
    self_reported_circulating_supply: int
    self_reported_market_cap: float
    tvl_ratio: Optional[float]
    last_updated: str
    quote: Quote