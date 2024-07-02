from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

DATASET_PATH = '../data/pricings_dataset.csv'

saas_list = [
    {
        "name": "ClickUp",
        "url": "https://clickup.com/pricing",
        "extended_pricing_button_text": "Complete feature list",
        "feature_elem": "tr",
        "feature_selector": {"class": True},
        "category": "Project Management",
        "product": ""
    },
    {
        "name": "HubSpot",
        "url": "https://www.hubspot.com/pricing/marketing/starter",
        "extended_pricing_button_text": "See all features and limits",
        "feature_elem": "th",
        "feature_selector": {"scope": "row"},
        "category": "CRM",
        "product": "Marketing - Individuals"
    },
    {
        "name": "Salesforce",
        "url": "https://www.salesforce.com/eu/sales/pricing/",
        "extended_pricing_button_text": "",
        "feature_elem": "div",
        "feature_selector": {"class": "table_column_header"},
        "category": "CRM",
        "product": "Sales"
    },
    # {
    #     "name": "Donorbox",
    #     "url": "https://donorbox.org/es/pricing",
    #     "extended_pricing_button_text": "",
    #     "feature_elem": "td",
    #     "feature_selector": {"data-label": None},
    #     "category": "Donation Management",
    #     "product": ""
    # },
    {
        "name": "Slack",
        "url": "https://slack.com/pricing",
        "extended_pricing_button_text": "",
        "feature_elem": "tr",
        "feature_selector": {"class": "o-pricing-table__row--feature"},
        "category": "Team Management",
        "product": ""
    },
    {
        "name": "Buffer",
        "url": "https://buffer.com/pricing",
        "extended_pricing_button_text": "",
        "feature_elem": "h4",
        "feature_selector": {},
        "category": "Social Media Management",
        "product": ""
    },
    {
        "name": "Hypercontext",
        "url": "https://hypercontext.com/pricing",
        "extended_pricing_button_text": "",
        "feature_elem": "div",
        "feature_selector": {"class": "inline"},
        "category": "Employee Engagement",
        "product": ""
    },
    {
        "name": "DocuSign",
        "url": "https://ecom.docusign.com/plans-and-pricing/esignature",
        "extended_pricing_button_text": "",
        "feature_elem": "button",
        "feature_selector": {"data-context": "show-features"},
        "category": "Digital Signature",
        "product": ""
    },
    {
        "name": "OpenPhone",
        "url": "https://www.openphone.com/pricing",
        "extended_pricing_button_text": "",
        "feature_elem": "div",
        "feature_selector": {"class": "price-table-row"},
        "category": "Business Phone System",
        "product": ""
    },
    {
        "name": "Pumble",
        "url": "https://pumble.com/pricing",
        "extended_pricing_button_text": "",
        "feature_elem": "span",
        "feature_selector": {"class": "first-cell"},
        "category": "Team Communication",
        "product": ""
    },
    {
        "name": "Tableau",
        "url": "https://www.tableau.com/pricing/teams-orgs",
        "extended_pricing_button_text": "",
        "feature_elem": "td",
        "feature_selector": {"class": "comparison-list__feature-description"},
        "category": "End-to-end Analytics",
        "product": "Teams-orgs"
    },
    {
        "name": "Quip",
        "url": "https://quip.com/about/pricing",
        "extended_pricing_button_text": "",
        "feature_elem": "td",
        "feature_selector": {"class": "td-first"},
        "category": "Document Management",
        "product": ""
    },
    {
        "name": "MailChimp",
        "url": "https://mailchimp.com/es/pricing/marketing/compare-plans/?currency=USD",
        "extended_pricing_button_text": "",
        "feature_elem": "tr",
        "feature_selector": {"class": ""},
        "category": "Marketing",
        "product": ""
    },
    # {
    #     "name": "Zapier",
    #     "url": "https://zapier.com/app/planbuilder/pricing",
    #     "extended_pricing_button_text": "",
    #     "feature_elem": "span",
    #     "feature_selector": {"data-testid": "iconContainer"},
    #     "category": "Automation & Cloud Integration",
    #     "product": ""
    # },
    {
        "name": "Deskera",
        "url": "https://www.deskera.com/pricing",
        "extended_pricing_button_text": "Show All Plan Features",
        "feature_elem": "tr",
        "feature_selector": {"class": "border-t border-t-prosaic-fawn dark:border-stone-800"},
        "category": "CRM",
        "product": "ERP"
    },
    {
        "name": "UserGuiding",
        "url": "https://userguiding.com/pricing",
        "extended_pricing_button_text": "Feature Comparison",
        "feature_elem": "div",
        "feature_selector": {"class": "feature-name-column"},
        "category": "User Onboarding",
        "product": ""
    },
    {
        "name": "PickFu",
        "url": "https://www.pickfu.com/pricing",
        "extended_pricing_button_text": "",
        "feature_elem": "div",
        "feature_selector": {"class": "col-5 p-0 col-desc"},
        "category": "Document Research",
        "product": ""
    },
    {
        "name": "Planable",
        "url": "https://planable.io/pricing/",
        "extended_pricing_button_text": "",
        "feature_elem": "div",
        "feature_selector": {"class": "pricing-table-row"},
        "category": "Social Media Management",
        "product": ""
    },
    {
        "name": "Databox",
        "url": "https://databox.com/pricing",
        "extended_pricing_button_text": "",
        "feature_elem": "span",
        "feature_selector": {"class": "feature__label"},
        "category": "Dashboard and Reporting",
        "product": ""
    },
    {
        "name": "Trustmary",
        "url": "https://trustmary.com/pricing/",
        "extended_pricing_button_text": "",
        "feature_elem": "tr",
        "feature_selector": {"class": "MuiTableRow-root css-104tjs9"},
        "category": "Surveys",
        "product": "Display"
    },
    {
        "name": "Evernote",
        "url": "https://evernote.com/compare-plans",
        "extended_pricing_button_text": "",
        "feature_elem": "td",
        "feature_selector": {"class": "flex flex-col pb-6 pt-8 text-left w-4/5"},
        "category": "Productivity",
        "product": ""
    },
    {
        "name": "Canva",
        "url": "https://www.canva.com/pricing/",
        "extended_pricing_button_text": "Comparar funciones",
        "feature_elem": "div",
        "feature_selector": {"class": "_9Mb__A ucVFnw hrs7_w iBrz7Q _9Jwa9A PbKupw"},
        "category": "Graphic Design",
        "product": ""
    },
    {
        "name": "Clockify",
        "url": "https://clockify.me/pricing",
        "extended_pricing_button_text": "",
        "feature_elem": "div",
        "feature_selector": {"class": "feature-content"},
        "category": "Time Tracking",
        "product": ""
    },
    {
        "name": "Figma",
        "url": "https://www.figma.com/pricing/",
        "extended_pricing_button_text": "",
        "feature_elem": "tr",
        "feature_selector": {"class": "css-lkm8k9"},
        "category": "Web Desing",
        "product": ""
    },
    {
        "name": "GitHub",
        "url": "https://github.com/pricing",
        "extended_pricing_button_text": "",
        "feature_elem": "div",
        "feature_selector": {"class": "flex-auto d-inline-block text-bold"},
        "category": "Version Control System",
        "product": ""
    },
    {
        "name": "Jira",
        "url": "https://www.atlassian.com/software/jira/pricing",
        "extended_pricing_button_text": "",
        "feature_elem": "tr",
        "feature_selector": {"class": "_80omtlke"},
        "category": "Project Management",
        "product": ""
    },
    {
        "name": "Microsoft 365",
        "url": "https://www.microsoft.com/en-us/microsoft-365/enterprise/office365-plans-and-pricing",
        "extended_pricing_button_text": "",
        "feature_elem": "tr",
        "feature_selector": {"class": "collapse material-surface text-left align-top"},
        "category": "Productivity",
        "product": "Enterprise"
    },
    {
        "name": "Monday",
        "url": "https://monday.com/pricing",
        "extended_pricing_button_text": "Lista completa de funciones",
        "feature_elem": "div",
        "feature_selector": {"class": "feature-name"},
        "category": "Productivity",
        "product": ""
    },
    {
        "name": "Postman",
        "url": "https://www.postman.com/pricing/",
        "extended_pricing_button_text": "",
        "feature_elem": "tr",
        "feature_selector": {"class": "zXcRd"},
        "category": "REST Client",
        "product": ""
    },
    {
        "name": "RapidAPI",
        "url": "https://rapidapi.com/products/pricing/",
        "extended_pricing_button_text": "",
        "feature_elem": "div",
        "feature_selector": {"class": "feature-item"},
        "category": "API Marketplace",
        "product": ""
    },
    {
        "name": "Rippling",
        "url": "https://www.rippling.com/es-ES/rippling-unity-tiers",
        "extended_pricing_button_text": "",
        "feature_elem": "div",
        "feature_selector": {"class": "row flex border-b-1 border-black border-opacity-20 flex-row compare-table-row"},
        "category": "HR Management",
        "product": "Unity"
    },
    {
        "name": "Wrike",
        "url": "https://www.wrike.com/comparison-table/",
        "extended_pricing_button_text": "",
        "feature_elem": "td",
        "feature_selector": {"class": "website-table__cell-description", "style": "width: 30%;"},
        "category": "Productivity",
        "product": ""
    },
]

test_list = []

if __name__ == '__main__':

    driver = webdriver.Chrome()
    driver.implicitly_wait(5)

    with open(DATASET_PATH, 'w') as f:
        f.write("name,extraction_date,number_of_features,category,url,product\n")

    for saas in saas_list:
        WEB_URL = saas["url"]
        EXTENDED_PRICING_BUTTON_TEXT = saas["extended_pricing_button_text"]
        FEATURE_ELEM = saas["feature_elem"]
        FEATURE_SELECTOR = saas["feature_selector"]

        driver.get(WEB_URL)

        if EXTENDED_PRICING_BUTTON_TEXT != "":
            elem = driver.find_element(By.XPATH, f"//*[text()='{EXTENDED_PRICING_BUTTON_TEXT}']")
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", elem)
            elem.click()
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        features = soup.find_all(FEATURE_ELEM, FEATURE_SELECTOR)

        with open(DATASET_PATH, 'a') as f:
            f.write(f"{saas['name']},{datetime.today().strftime('%Y-%m-%d')},{len(features)},{saas['category']},{saas['url']},{saas['product']}\n")

    driver.close()