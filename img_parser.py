import http.client
import urllib.parse
import os
from io import BytesIO
from html.parser import HTMLParser

# Извлечение ссылок на картинки
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
                    if not attr[1].startswith("http"):
                        full_image_url = urllib.parse.urljoin(self.url, attr[1])
                    else:
                        full_image_url = attr[1]

                    self.images.append(full_image_url)

# Извлечение ссылок на другие страницы
class LinkParser(HTMLParser):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    full_link = urllib.parse.urljoin(self.url, attr[1])
                    self.links.append(full_link)

def download_images_httpclient(url, output_dir="images"):
    try:
        parsed_url = urllib.parse.urlparse(url)
        conn = http.client.HTTPConnection(parsed_url.netloc)
        conn.request("GET", parsed_url.path)
        response = conn.getresponse()
        html_content = response.read().decode('utf-8', errors='ignore')
        conn.close()

        link_parser = LinkParser(url)
        link_parser.feed(html_content)

        for link_url in link_parser.links:
            try:
                download_images_from_url(link_url, output_dir)
            except Exception as e:
                print(f"Ошибка при скачивании из {link_url}: {e}")

        image_extractor = ImageExtractor(url, output_dir)
        image_extractor.feed(html_content)
        for img_url in image_extractor.images:
            try:
                download_image(img_url, output_dir)
            except Exception as e:
                print(f"Ошибка при скачивании изображения {img_url}: {e}")

    except (http.client.HTTPException, OSError, UnicodeDecodeError) as e:
        print(f"Ошибка при скачивании с {url}: {e}")
        return

# Скачивание изображения с указанного URL
def download_images_from_url(url, output_dir):
  try:
      parsed_url = urllib.parse.urlparse(url)
      conn = http.client.HTTPConnection(parsed_url.netloc)
      conn.request("GET", parsed_url.path)
      response = conn.getresponse()
      html_content = response.read().decode('utf-8', errors='ignore')
      conn.close()

      image_extractor = ImageExtractor(url, output_dir)
      image_extractor.feed(html_content)
      for img_url in image_extractor.images:
          try:
              download_image(img_url, output_dir)
          except Exception as e:
              print(f"Ошибка при скачивании изображения {img_url}: {e}")
  except Exception as e:
        print(f"Ошибка при скачивании с {url}: {e}")
        return

# Скачивание одного изображения
def download_image(img_url, output_dir):
    try:
        parsed_img_url = urllib.parse.urlparse(img_url)
        conn = http.client.HTTPConnection(parsed_img_url.netloc)
        conn.request("GET", parsed_img_url.path)
        img_response = conn.getresponse()
        img_data = img_response.read()
        conn.close()
        filename = os.path.join(output_dir, os.path.basename(parsed_img_url.path))
        os.makedirs(output_dir, exist_ok=True)
        with open(filename, "wb") as f:
            f.write(img_data)
            print(f"Изображение сохранено: {filename}")
    except (http.client.HTTPException, OSError, UnicodeDecodeError) as e:
        print(f"Ошибка при загрузке изображения {img_url}: {e}")

if __name__ == "__main__":
    url = ""
    download_images_httpclient(url)