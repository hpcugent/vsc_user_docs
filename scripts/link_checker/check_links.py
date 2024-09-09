import aiohttp
import asyncio
import argparse


# Logic for checking status codes of URLs

async def fetch_status_codes(urls: list[str], timeout: int):
    """
    Asynchronously fetch the status codes of each URL in a list.

    :param urls: The URLs to check
    :param timeout: The maximum time to wait for each request
    :return: A list of status codes
    """
    connector = aiohttp.TCPConnector(limit=None)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = (fetch_status_code(session, url, timeout) for url in urls)
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses


async def fetch_status_code(session: aiohttp.ClientSession, url: str, timeout: int) -> int | str:
    """
    Fetch the status code of a URL.
    :param session: The aiohttp session
    :param url: The URL to check
    :param timeout: The maximum time to wait for the request
    :return: The status code, the string "Timeout" if the request timed out, or "Error" if an error occurred
    """
    try:
        async with session.get(url, timeout=timeout) as response:
            status = response.status
    except asyncio.TimeoutError:
        status = "Timeout"
    except aiohttp.ClientError:
        status = "Error"

    return status


# Logic for reading input files

def read_url_file(filename: str, whitelist: set[str] = None) -> tuple[list[str], list[str]]:
    """
    Read a file containing URLs to check. The file should contain one URL per line.

    :param filename:
    :param whitelist:
    :return:
    """
    paths, urls = [], []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            url_file, url = line.split(maxsplit=1)  # Split on first space
            if not whitelist or url not in whitelist:
                paths.append(url_file)
                urls.append(url)
    return paths, urls


def read_whitelist(filename: str) -> set[str]:
    """
    Read a file containing URLs to ignore. The file should contain one URL per line.

    :param filename: The file to read
    :return: A set of URLs to ignore
    """
    if not filename:
        return set()

    with open(filename, 'r') as file:
        return {line.strip() for line in file}


def main(url_file, timeout, whitelist=None):
    """
    Check status codes of URLs. Output status codes that are not 200 OK.
    """
    whitelist = read_whitelist(whitelist)
    paths, urls = read_url_file(url_file, whitelist)
    status_codes = asyncio.run(fetch_status_codes(urls, timeout))

    grouped = {}
    for path, url, status_code in zip(paths, urls, status_codes):
        grouped.setdefault(status_code, []).append((path, url))

    # Print results
    ok = grouped.pop(200, [])
    print(f"{len(ok)} links have status code 200 OK.\n")
    for key in grouped.keys():
        print(key)
        for path, url in grouped[key]:
            print(f'  {path}: {url}')
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check status codes of URLs')
    parser.add_argument('url_file', nargs='?', type=str, help='File containing URLs to check (omit to read from stdin)')
    parser.add_argument('--timeout', type=int, default=7, help='Timeout for each request')
    parser.add_argument('--whitelist', type=str, help='File containing URLs to ignore')

    args = parser.parse_args()
    main(args.url_file, args.timeout, args.whitelist)
