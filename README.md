# Web Crawler

This project is a simple web crawler that visits URLs and extracts the visible text from each page. It's written in Python, and uses the requests library to download webpages, BeautifulSoup to parse them, and csv to write the results to a file.

## How it works

The crawler starts with a list of URLs to visit. It pops an URL from the list, downloads its content, and extracts all the visible text, which is then saved in a CSV file.

Next, it parses the HTML to find all linked URLs. These new URLs are added to the list of URLs to visit, if they have not been visited already. This process repeats until there's no URL left to visit.

There's a delay of 1 second introduced between each request to prevent overwhelming the server with too many requests in a short amount of time.

## How to run

1. First, install the required dependencies by running:

```sh
pip install -r requirements.txt
```

2. Then, you can run the script with:

```sh
python crawler.py
```

By default, the script will start crawling from 'https://www.imdb.com'. You can change the starting URLs by modifying the list passed to the Crawler's constructor in the script.

```python
Crawler(urls=['https://www.example.com']).run()
```

The results will be saved into multiple text files named after each webpage scrapped. Each line of the file contains the extracted text from that URL.

## Logging

The script uses Python's logging library to log the progress of the crawler. INFO level messages are printed to the console, and ERROR level messages are saved to a file named 'file.log'.
