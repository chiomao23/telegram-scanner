import iocextract


def extract_iocs(text):
    if not text:
        return []

    found = []

    for ip in iocextract.extract_ips(text, refang=True):
        found.append(("ip", ip))

    for url in iocextract.extract_urls(text, refang=True):
        found.append(("url", url))

    for md5 in iocextract.extract_md5_hashes(text):
        found.append(("md5", md5))

    for sha1 in iocextract.extract_sha1_hashes(text):
        found.append(("sha1", sha1))

    for sha256 in iocextract.extract_sha256_hashes(text):
        found.append(("sha256", sha256))

    for email in iocextract.extract_emails(text, refang=True):
        found.append(("email", email))

    return found


if __name__ == "__main__":
    sample = """
    New dump available: hxxp://evil-domain[.]com/download
    IP: 185.220.101[.]45
    Hash: 5d41402abc4b2a76b9719d911017c592
    Contact: fakebuyer@protonmail.com
    """
    results = extract_iocs(sample)
    print("Found IOCs:")
    for ioc_type, ioc_value in results:
        print(f"  [{ioc_type}] {ioc_value}")
