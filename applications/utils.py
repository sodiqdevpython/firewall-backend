import requests


def ip_lookup_online(ip):
    url = f"http://ip-api.com/json/{ip}"
    resp = requests.get(url).json()
    return {
        "ip": ip,
        "hostname": resp.get("reverse"),
        "asn": resp.get("as"),
        "isp": resp.get("isp"),
        "country": resp.get("country"),
        "region": resp.get("regionName"),
        "city": resp.get("city"),
        "latitude": resp.get("lat"),
        "longitude": resp.get("lon")
    }
