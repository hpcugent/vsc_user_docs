import aiohttp
import asyncio
import argparse

from aiohttp import ClientTimeout


# Logic for checking status codes of URLs

async def fetch_status_codes(urls: list[str]):
    """
    Asynchronously fetch the status codes of each URL in a list.

    :param urls: The URLs to check
    :return: A list of status codes
    """
    async with aiohttp.ClientSession() as session:
        tasks = (fetch_status_code(session, url) for url in urls)
        return await asyncio.gather(*tasks, return_exceptions=True)


async def fetch_status_code(session: aiohttp.ClientSession, url: str):
    """
    Fetch the status code of a URL.
    :param session: The aiohttp session
    :param url: The URL to check
    :return: The status code, the string "Timeout" if the request timed out, or "Error" if an error occurred
    """
    async with session.get(url) as response:
        return response.status


# Logic for reading input files

def read_url_file(filename: str, whitelist: set[str]) -> tuple[list[str], list[str]]:
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
            if url not in whitelist:
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


def main(url_file, whitelist=None):
    """
    Check status codes of URLs. Output status codes that are not 200 OK.
    """
    whitelist = read_whitelist(whitelist)
    paths, urls = read_url_file(url_file, whitelist)
    status_codes = asyncio.run(fetch_status_codes(urls))

    # Group URLs by status code
    grouped = {}
    for path, url, status in zip(paths, urls, status_codes):
        if isinstance(status, Exception):
            url += f" ({status})"  # Add error message to URL
            status = "Error"  # will group under common "Error" key
        grouped.setdefault(status, []).append((path, url))

    # Print results
    print("=" * 80)
    ok = grouped.pop(200, [])
    print(f"{len(ok)} links have status code 200 OK.\n")
    for key in grouped.keys():
        print(key)
        for path, url in grouped[key]:
            print(f'{path} : {url}')
        print()

    # Exit with error code if any non-200 status codes were found
    if grouped:
        print(f"Found {len(urls) - len(ok)} links with non-200 status codes.")
        exit(1)
    else:
        print("All links are OK.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check status codes of URLs')
    parser.add_argument('url_file', nargs='?', type=str, help='File containing URLs to check (omit to read from stdin)')
    parser.add_argument('--whitelist', type=str, help='File containing URLs to ignore')

    args = parser.parse_args()
    main(args.url_file, args.whitelist)
