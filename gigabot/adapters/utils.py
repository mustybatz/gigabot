from typing import Any, Dict
from gigabot.adapters.models.crypto_quote import CryptocurrencyQuote, Tag, Platform, QuoteDetail, Quote
from gigabot.adapters.models.coin_info import CoinInfo, ContractAddress, URLs

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

def create_coin_info(data: Dict[str, Any]) -> CoinInfo:
    # Extract tag_names and tag_groups with defaults if they are not present
    tag_names = data.pop('tag-names', [])
    tag_groups = data.pop('tag-groups', [])

    # Create URLs object from nested data and remove it from data dictionary
    urls = URLs(**data.pop('urls'))

    # Handle platform data separately if it exists
    platform_data = data.pop('platform', None)
    platform = Platform(**platform_data) if platform_data else None

    # Handle contract_address separately and ensure it's not in the data when unpacking to CoinInfo
    contract_addresses_data = data.pop('contract_address', [])
    contract_addresses = [ContractAddress(**ca) for ca in contract_addresses_data]

    # Create the CoinInfo object ensuring no duplicate 'contract_address' argument
    return CoinInfo(
        tag_names=tag_names,
        tag_groups=tag_groups,
        urls=urls,
        platform=platform,
        contract_address=contract_addresses,
        **data
    )
