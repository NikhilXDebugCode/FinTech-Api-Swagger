import traceback
import sys

try:
    import httpx
    print("httpx imported successfully")
except Exception as e:
    with open("cgi_err.txt", "w") as f:
        traceback.print_exc(file=f)
    print("Error captured in cgi_err.txt")
