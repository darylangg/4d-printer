url = "https://www.singaporepools.com.sg/DataFileArchive/Lottery/Output/fourd_result_top_draws_en.html"

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from datetime import date, datetime
from weasyprint import HTML, CSS
import requests
import cups

def scrape_results(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")   # or "html.parser"
    draw_date = soup.select_one("th.drawDate").get_text(strip=True)
    first_prize = soup.select_one("td.tdFirstPrize").get_text(strip=True)
    second_prize = soup.select_one("td.tdSecondPrize").get_text(strip=True)
    third_prize = soup.select_one("td.tdThirdPrize").get_text(strip=True)

    latest_starter_body = soup.select_one("tbody.tbodyStarterPrizes")

    starters = [
        td.get_text(strip=True)
        for td in latest_starter_body.find_all("td")
    ]

    latest_consol_body = soup.select_one("tbody.tbodyConsolationPrizes")

    consolations = [
        td.get_text(strip=True)
        for td in latest_consol_body.find_all("td")
    ]

    dt = datetime.strptime(draw_date, "%a, %d %b %Y")
    today = date.today()

    mandarin_weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    
    return {
        "date": f"{dt.year}年 {dt.month}月 {dt.day}日",
        "day": mandarin_weekdays[dt.weekday()],
        "winners": [first_prize, second_prize, third_prize],
        "starters": [starters[:5], starters[5:]],
        "consolations": [consolations[:5], consolations[5:]],
        "print_date": today.strftime("%d %b %Y")
    }

def write_to_pdf(results, template_path):
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template('results.html')
    rendered_html = template.render(results)
    today = date.today()
    formatted_date = today.strftime("%Y%m%d")
    HTML(string=rendered_html).write_pdf(
        "archive/" + formatted_date + ".pdf",
        stylesheets=[CSS( template_path + "/style.css")]
        )

def print_pdf():
    today = date.today()
    formatted_date = today.strftime("%Y%m%d")
    conn = cups.Connection()
    printers = conn.getPrinters()
    default_printer = conn.getDefault()
    job_id = conn.printFile(
        default_printer,
        "archive/" + formatted_date + ".pdf",
        formatted_date + "4D Results",
        {}
    )
    print("adding " + str(job_id) + " to print queue")

results = scrape_results(url)
write_to_pdf(results, "template")
print_pdf()