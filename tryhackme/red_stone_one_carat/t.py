import urllib.request

for port in range(80,20000):
    print("\n", port)
    try:
        print(urllib.request.urlopen(f"http://127.0.0.1:{port}").read())
        print(f"Port {port} Working !")
        break
    except:
        print("error")

