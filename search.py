import argparse
from database import search_messages, search_iocs

parser = argparse.ArgumentParser(description="Search collected Telegram data")
parser.add_argument("--keyword", help="Search messages containing this word")
parser.add_argument(
    "--iocs",
    nargs="?",
    const="ALL",
    help="Show extracted IOCs. Optionally filter by type: ip, url, md5, sha1, sha256, email",
)
args = parser.parse_args()

if args.keyword:
    results = search_messages(args.keyword)
    print(f"\nFound {len(results)} message(s) containing '{args.keyword}':\n")
    for row in results:
        print(f"[{row['channel']}] {row['timestamp']}")
        print(f"  {row['text'][:200]}")
        print()

if args.iocs:
    ioc_type = None if args.iocs == "ALL" else args.iocs
    results = search_iocs(ioc_type)
    label = f"type='{ioc_type}'" if ioc_type else "all types"
    print(f"\nFound {len(results)} IOC(s) ({label}):\n")
    for row in results:
        print(f"  [{row['ioc_type']}] {row['ioc_value']}")

if not args.keyword and not args.iocs:
    parser.print_help()
