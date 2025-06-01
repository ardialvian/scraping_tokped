from playwright.sync_api import sync_playwright
import pandas as pd
import time

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
url = 'https://www.tokopedia.com/search?st=&q=hoodie&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource='

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    context = browser.new_context(user_agent=user_agent)
    page = context.new_page()
    page.goto(url)

    for _ in range(20):
        page.mouse.wheel(0,1000)
        time.sleep(2)

    page.wait_for_selector('a[class*="IM26HEnTb-krJayD-R0OHw"]')
    products = page.query_selector_all('a[class*="IM26HEnTb-krJayD-R0OHw"]')
    data = []

    for product in products:
        try:
            product_element = product.query_selector('span[class*="_0T8-iGxMpV6NEsYEhwkqEg"]')
            product_name = product_element.inner_text().strip() if product_element else ''
            price_element = product.query_selector('div[class*="_67d6E1xDKIzw+i2D2L0tjw"]')
            price = price_element.inner_text().strip() if price_element else ''
            sold_element = product.query_selector('span[class*="se8WAnkjbVXZNA8mT+Veuw"]')
            sold = sold_element.inner_text().strip() if sold_element else 'Not yet Sold'

            data.append({
                'product_name': product_name,
                'price': price,
                'sold': sold
            })

        except Exception as e:
            print(f"pharsing error: {e}")

    df = pd.DataFrame(data)
    df.to_csv(f"scraping_tokped.csv", index=False, encoding="utf-8-sig")
    print(f"scraping has done")