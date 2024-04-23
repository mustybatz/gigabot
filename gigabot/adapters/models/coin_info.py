from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Status:
    timestamp: str
    error_code: int
    error_message: Optional[str]
    elapsed: int
    credit_count: int
    notice: Optional[str]

@dataclass
class Platform:
    name: str
    id: str
    slug: str
    symbol: str
    token_address: str

@dataclass
class Coin:
    id: str
    name: str
    symbol: str
    slug: str

@dataclass
class CoinPlatform:
    name: str
    coin: Coin

@dataclass
class ContractAddress:
    contract_address: str
    platform: Platform

@dataclass
class URLs:
    website: List[str]
    twitter: List[str]
    message_board: List[str]
    chat: List[str]
    facebook: List[str]
    explorer: List[str]
    reddit: List[str]
    technical_doc: List[str]
    source_code: List[str]
    announcement: List[str]

@dataclass
class CoinInfo:
    id: int
    name: str
    symbol: str
    category: str
    description: str
    slug: str
    logo: str
    subreddit: str
    notice: str
    tags: List[str]
    tag_names: List[str]
    tag_groups: List[str]
    urls: URLs
    platform: Optional[Platform]  # Made optional to accommodate coins without a platform
    date_added: str
    twitter_username: str
    is_hidden: int
    date_launched: Optional[str]  # Made optional for coins that might not have this info
    contract_address: List[ContractAddress]
    self_reported_circulating_supply: int
    self_reported_tags: Optional[List[str]]
    self_reported_market_cap: float
    infinite_supply: bool

