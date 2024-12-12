import http.client

def fetch_page(url):
    try:
        parsed_url = url.split("://", 1)[1] 
        host, path = parsed_url.split("/", 1)
        conn = http.client.HTTPConnection(host)
        conn.request("GET", "/" + path) 
        response = conn.getresponse()
        print("Статус ответа:", response.status, response.reason)
        print("Заголовки ответа:\n", response.headers)
        data = response.read()
        print("\nКонтент страницы (первые 500 байт):\n", data[:500].decode('utf-8', errors='ignore')) 
        conn.close()
    except (http.client.HTTPException, ValueError, UnicodeDecodeError) as e:
        print(f"Ошибка при загрузке страницы: {e}")
    except Exception as e: 
        print(f"Произошла неизвестная ошибка: {e}")

if __name__ == "__main__":
    url = ""
    fetch_page(url)