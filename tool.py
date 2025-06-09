import socket
import sys
import requests
from colorama import init, Fore

init(autoreset=True)

def get_ip_from_url(url):
    try:
        if url.startswith("http://") or url.startswith("https://"):
            url = url.split("//")[1]
        url = url.split("/")[0]
        ip = socket.gethostbyname(url)
        return ip
    except socket.gaierror:
        return None

def get_geolocation(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = response.json()
        if data["status"] == "success":
            return {
                "country": data["country"],
                "region": data["regionName"],
                "city": data["city"],
                "isp": data["isp"],
                "lat": data["lat"],
                "lon": data["lon"]
            }
        else:
            return None
    except requests.RequestException:
        return None

def main():
    print(Fore.GREEN + "=== URL to IP + Geolocation ===")
    while True:
        url = input(Fore.GREEN + "\nEnter a URL (e.g. example.com or https://example.com): ").strip()
        ip = get_ip_from_url(url)

        if ip:
            print(Fore.GREEN + f"[+] IP Address of '{url}': {ip}")
            geo = get_geolocation(ip)
            if geo:
                print(Fore.GREEN + f"    └ Country: {geo['country']}")
                print(Fore.GREEN + f"    └ Region : {geo['region']}")
                print(Fore.GREEN + f"    └ City   : {geo['city']}")
                print(Fore.GREEN + f"    └ ISP    : {geo['isp']}")
                print(Fore.GREEN + f"    └ Coords : {geo['lat']}, {geo['lon']}")
            else:
                print(Fore.GREEN + "[!] Could not fetch geolocation data.")
        else:
            print(Fore.GREEN + f"[-] Could not resolve IP for: {url}")

        choice = input(Fore.GREEN + "\nDo you want to convert another URL? (y/n): ").strip().lower()
        if choice != 'y':
            print(Fore.GREEN + "Exiting...")
            sys.exit()

if __name__ == "__main__":
    main()
