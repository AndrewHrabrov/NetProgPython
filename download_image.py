import http.client
import urllib.parse
import os
from html.parser import HTMLParser

class ImageExtractor(HTMLParser):
    def __init__(self, url, output_dir):
        super().__init__()
        self.url = url
        self.output_dir = output_dir
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            for attr in attrs:
                if attr[0] == "src":
                    self.images.append(attr[1])


def download_images_httpclient(url, output_dir="images"):
    try:
        parsed_url = urllib.parse.urlparse(url)
        conn = http.client.HTTPConnection(parsed_url.netloc)
        conn.request("GET", parsed_url.path)
        response = conn.getresponse()
        html_content = response.read().decode('utf-8', errors='ignore')
        conn.close()

        extractor = ImageExtractor(url, output_dir)
        extractor.feed(html_content)
        os.makedirs(output_dir, exist_ok=True)

        for img_url in extractor.images:
            img_url = urllib.parse.urljoin(url, img_url)
            try:
                parsed_img_url = urllib.parse.urlparse(img_url)
                conn = http.client.HTTPConnection(parsed_img_url.netloc)
                conn.request("GET", parsed_img_url.path)
                img_response = conn.getresponse()
                img_data = img_response.read()
                conn.close()

                filename = os.path.join(output_dir, os.path.basename(parsed_img_url.path))
                with open(filename, "wb") as f:
                    f.write(img_data)
                print(f"Изображение сохранено: {filename}")

            except (http.client.HTTPException, OSError, UnicodeDecodeError) as e:
                print(f"Ошибка при загрузке изображения {img_url}: {e}")

    except (http.client.HTTPException, OSError) as e:
        print(f"Ошибка при загрузке страницы: {e}")


if __name__ == "__main__":
    url = ""
    download_images_httpclient(url)