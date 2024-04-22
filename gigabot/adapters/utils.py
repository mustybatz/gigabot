from typing import Dict
from adapters.models import CryptocurrencyQuote, Tag, Platform, QuoteDetail, Quote

def create_cryptocurrency_quote(data: Dict) -> CryptocurrencyQuote:
    # This function assumes that all keys are present and correctly formatted in the data.
    tags = [Tag(**tag) for tag in data['tags']]
    platform = Platform(**data['platform'])
    quote_detail = QuoteDetail(**data['quote']['USD'])
    quote = Quote(USD=quote_detail)
    
    return CryptocurrencyQuote(
        id=data['id'],
        name=data['name'],
        symbol=data['symbol'],
        slug=data['slug'],
        num_market_pairs=data['num_market_pairs'],
        date_added=data['date_added'],
        tags=tags,
        max_supply=data['max_supply'],
        circulating_supply=data['circulating_supply'],
        total_supply=data['total_supply'],
        platform=platform,
        is_active=data['is_active'],
        infinite_supply=data['infinite_supply'],
        cmc_rank=data['cmc_rank'],
        is_fiat=data['is_fiat'],
        self_reported_circulating_supply=data['self_reported_circulating_supply'],
        self_reported_market_cap=data['self_reported_market_cap'],
        tvl_ratio=data['tvl_ratio'],
        last_updated=data['last_updated'],
        quote=quote
    )
