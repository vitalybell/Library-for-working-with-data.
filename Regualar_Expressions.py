import re


def extract_image_links(html_text):
    pattern = r'<img.*?src=["\'](.*?)["\'].*?>'
    image_links = re.findall(pattern, html_text, re.IGNORECASE)

    # Фильтруем ссылки по расширениям .jpg, .jpeg, .png и .gif
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    image_links = [link for link in image_links if any(ext in link.lower() for ext in valid_extensions)]

    return image_links

# Например:


sample_html = "<img src='https://example.com/image1.jpg'> <img src='http://example.com/image2.png'> <img src='https://example.com/image3.gif'>"

image_links = extract_image_links(sample_html)
if image_links:
  for image_link in image_links:
    print(image_link)
else:
  print("Нет ссылок с картинками в HTML тексте.")
