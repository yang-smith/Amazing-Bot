api_prices = {
    'gpt-3.5-turbo': {
        'price_per_thousand_input': 0.00225,
        'price_per_thousand_output': 0.003,
        'max_tokens': 16384
    },
    'gpt-3.5-turbo-16k': {
        'price_per_thousand_input': 0.0045,
        'price_per_thousand_output': 0.006,
        'max_tokens': 16384
    },
    'gpt-4-1106-preview': {
        'price_per_thousand_input': 0.0225,
        'price_per_thousand_output': 0.045,
        'max_tokens': 128000
    },
    'gpt-4': {
        'price_per_thousand_input': 0.045,
        'price_per_thousand_output': 0.09,
        'max_tokens': 8192
    },
    'gpt-4-32k': {
        'price_per_thousand_input': 0.09,
        'price_per_thousand_output': 0.18,
        'max_tokens': 32768
    },
    'claude-2': {
        'price_per_thousand_input': 0.02204,
        'price_per_thousand_output': 0.06536,
        'max_tokens': 100000
    }
}

def calculate_price(api_type, token_count, is_input=True):
    if api_type in api_prices:
        price_info = api_prices[api_type]
        if is_input:
            price_per_thousand = price_info['price_per_thousand_input']
        else:
            price_per_thousand = price_info['price_per_thousand_output']
        price = price_per_thousand * (token_count / 1000)
        return price
    else:
        return None