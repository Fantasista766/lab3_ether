from web3 import Web3
import asyncio

from main import token_contract


def handle_event(event):
    """Обрабатывает полученные по подписке события"""
    print('EVENT IN eventSubscription file')
    print(Web3.to_json(event))


async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(poll_interval)


def main():
    # г) подписка на события
    event_filter = token_contract.events.Transfer.create_filter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
    finally:
        loop.close()


if __name__ == '__main__':
    main()

