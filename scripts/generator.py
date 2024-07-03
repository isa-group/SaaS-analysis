import google.generativeai as genai
from dotenv import load_dotenv
from selenium import webdriver
from logconf import log_setup
import logging
import os, pathlib, time, argparse, re

load_dotenv()
log_setup()

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
PROMPT_PATH = os.path.join(BASE_PATH, 'prompt')
PRICINGS_PATH = os.path.join(os.pardir, 'pricings')
MODEL = 'gemini-1.5-flash' # 'gemini-1.5-flash' or 'gemini-1.5-pro'

if not os.path.exists(os.path.join(BASE_PATH, 'logs')):
    os.makedirs(os.path.join(BASE_PATH, 'logs'))

logger = logging.getLogger(name=f'log-{str(time.time())}')
    
def get_html(url:str) -> str:
    driver_options = webdriver.ChromeOptions()
    driver_options.headless = False
    driver = webdriver.Chrome(options=driver_options)
    driver.implicitly_wait(2)
    driver.get(url)
    page_content = driver.page_source
    driver.quit()
    return page_content

def read_file(filepath:str, as_list:bool = True) -> list[str] | str:
    if as_list:
        with open(filepath) as f:
            content = f.read().splitlines()
    else:
        with open(filepath) as f:
            content = f.read()
    return content

def get_images() -> list[dict]:
    images = os.listdir(PROMPT_PATH)
    return [build_image(os.path.join(PROMPT_PATH, image)) for image in images if image.endswith('.png')]

def build_image(path:str) -> dict:
    return {'mime_type': 'image/png', 'data': pathlib.Path(path).read_bytes()}

def build_prompt(next_html:str, previous_html:str, previous_yml:str, previous_file_name:str, next_file_name:str, saas_name:str, year:int, previous_year:int) -> str:
    
    first_example_file_name = 'github2023'
    second_example_file_name = 'postman2023'
    
    context = read_file(os.path.join(PROMPT_PATH, 'context.txt'))
    github_2023 = read_file(os.path.join(PROMPT_PATH, first_example_file_name+'.html'))
    github_yml_2019 = read_file(os.path.join(PROMPT_PATH, first_example_file_name+'.yml'))
    postman_2023 = read_file(os.path.join(PROMPT_PATH, second_example_file_name+'.html'))
    postman_yml_2023 = read_file(os.path.join(PROMPT_PATH, second_example_file_name+'.yml'))
    
    prompt = f"""You have to generate a yaml file that models the SaaS pricing of {saas_name} that is contained in the HTML file: {next_file_name}.html.

    As an  example of a real application of this YAML specification, you will be provided with the HTML file for the GitHub pricing: {first_example_file_name}.html and the Postman pricing: {second_example_file_name}.html for which it has been modeled their respective YAML specification: {first_example_file_name}.yml and {second_example_file_name}.yml.
    Furthermore, you will be provided with the YAML specification for the {saas_name} pricing of {str(previous_year)}: {previous_file_name}.yml and its HTML counterpart from where the pricing data was extracted: {previous_file_name}.html.
    The file you have to model must include all the features, usagesLimits, plans and addOns extracted from the HTML like the GitHub and Postman examples do, but you must remember that the HTML are different so, the content of the YAML generated will be also different. Moreover, the same caution must be taken with the {saas_name} {str(previous_year)} YAML specification, as it is quite different from the {saas_name} {str(year)} HTML file (althought it is true that their content could be more aligned).

    The explanation about the YAML specification, including its rules and structure: '''{context}'''
    
    The figures mentioned in the previous context are passed in the query as images. These images include several excerpts of the pricings used as examples and an UML diagram that models the full specificaction and structure.

    The file {first_example_file_name}.html has the following content:
    '''{github_2023}'''
    
    The file {first_example_file_name}.yml has the following content and structure:
    '''{github_yml_2019}'''
    
    The file {second_example_file_name}.html has the following content:
    '''{postman_2023}'''
    
    The file {second_example_file_name}.yml has the following content and structure:
    '''{postman_yml_2023}'''
    
    The file {previous_file_name}.html has the following content:
    '''{previous_html}'''
    
    The file {previous_file_name}.yml has the following content and structure:
    '''{previous_yml}'''

    The file {next_file_name}.html has the following content:
    '''{next_html}'''
    """
    return prompt

def get_file(saas_name:str, previous_year: int) -> str | FileNotFoundError:
    folder = os.path.join(PRICINGS_PATH, str(previous_year))
    files_list = os.listdir(folder)
    for file in files_list:
        if saas_name.lower().strip() == file.lower().replace('.yml', '').strip():
            return os.path.join(folder, file)
    raise FileNotFoundError(f"File {saas_name} not found in {folder}")

def build_output_path(saas_name:str, year:int) -> str:
    if not os.path.exists(os.path.join(PRICINGS_PATH, str(year))):
        os.mkdir(os.path.join(PRICINGS_PATH, str(year)))
    return os.path.join(PRICINGS_PATH, str(year), f"{saas_name.lower().strip()}.yml")

def write_file(filepath:str, content:str):
    with open(filepath, 'w') as f:
        f.write(content)
        
def generate_answer(model:str, prompt:str, images:list[dict]) -> str:
    genai.configure(api_key=os.getenv('GOOGLE_AI_STUDIO'))
    
    response = genai.GenerativeModel(model).generate_content(contents=[prompt, *images])
    
    return response.text

def post_process(response_text:str) -> str:
    response_text = response_text.strip()
    
    if response_text.startswith("\n"):
        response_text = response_text[1:]
    
    if response_text.endswith("\n"):
        response_text = response_text[:len(response_text)-1]
        
    response_text = response_text.strip()
    
    if response_text.startswith("```yaml"):
        response_text = response_text.replace("```yaml", '')
    
    if response_text.endswith("```"):
        response_text = response_text.replace("```", '')
    
    response_text = response_text.strip()
    
    if response_text.startswith("\n"):
        response_text = response_text[1:]
    
    if response_text.endswith("\n"):
        response_text = response_text[:len(response_text.strip())-1]
    
    return response_text.strip()

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Generate a YAML file from a SaaS pricing HTML file.')
    
    parser.add_argument('--saas_name', type=str, help='The name of the SaaS service to model.')
    parser.add_argument('--year', type=int, help='The year of the pricing to model.')
    parser.add_argument('--html_url', type=str, help='The URL of the HTML file that includes the pricing to model.')
    parser.add_argument('--previous_html_url', type=str, help='The URL of the HTML file that includes the pricing of the previous year.')
    parser.add_argument('--year-gap', type=int, help='The gap between the year of the pricing to model and the previous year.', default=1)
    
    args = parser.parse_args()
    return args

def check_args(saas_name:str, year:int, html_url:str, previous_html_url:str, year_gap:int) -> int:
    if not saas_name:
        raise ValueError("The saas_name argument is required.")
    if not year:
        raise ValueError("The year argument is required.")
    if not html_url:
        raise ValueError("The html_url argument is required.")
    if not previous_html_url:
        raise ValueError("The previous_html_url argument is required.")
    if not year_gap:
        year_gap = 1
        
    if year > time.localtime().tm_year:
        raise ValueError("The year argument must be less than the current year.")
    if year - year_gap > time.localtime().tm_year:
        raise ValueError("The year argument minus the year_gap argument must be less than the current year.")
    if year <= 1970:
        raise ValueError("The year argument must be greater than 1970.")
    if year - year_gap <= 1970:
        raise ValueError("The year argument minus the year_gap argument must be greater than 1970.")
    
    if not is_valid_url(html_url):
        raise ValueError("The html_url argument must be a valid URL.")
    if not is_valid_url(previous_html_url):
        raise ValueError("The previous_html_url argument must be a valid URL.")
    
    return year_gap

def is_valid_url(url:str) -> bool:
    url_pattern = re.compile(
        r'^(https?://)?'                      # Optional http or https scheme
        r'((([A-Za-z0-9-]+)\.)+[A-Za-z]{2,})'  # Domain name
        r'(:\d+)?'                             # Optional port
        r'(\/[A-Za-z0-9-._~:/?#[@\]!$&\'()*+,;=]*)?$'  # Optional path and query
    )

    return re.fullmatch(url_pattern, url) is not None

def main():
    start_time = time.time()
    args = get_args()
    
    saas_name = str(args.saas_name).strip()
    year = int(args.year)
    html_url = str(args.html_url).strip()
    previous_html_url = str(args.previous_html_url).strip()
    year_gap = int(args.year_gap)
    
    year_gap = check_args(saas_name, year, html_url, previous_html_url, year_gap)
    
    logger.info(f"Starting execution for {saas_name} pricing of {year}...")
    
    previous_year = year - year_gap
    previous_yml_path = get_file(saas_name, previous_year)
    logger.info(f"Getting HTML content from {html_url}...")
    next_html = get_html(html_url)
    logger.info(f"Getting HTML content from {previous_html_url}...")
    previous_html = get_html(previous_html_url)
    previous_yml = read_file(previous_yml_path)
    next_yml_path = build_output_path(saas_name, year)
    previous_file_name = f"{saas_name.lower().strip()}{previous_year}"
    next_file_name = f"{saas_name.lower().strip()}{year}"
    
    prompt = build_prompt(next_html, previous_html, previous_yml, previous_file_name, next_file_name, saas_name, year, previous_year)
    images = get_images()
    logger.info(f"Prompt: {prompt}")
    
    logger.info(f"Evaluating model {MODEL}...")
    
    new_start_time = time.time()
    response_text = generate_answer(MODEL, prompt, images)
    
    logger.info(f"Response: {response_text}")
    logger.info(f"Response obtained in {time.time()-new_start_time} seconds.")
    
    result = post_process(response_text)
    write_file(next_yml_path, result)
    
    end_time = time.time()
    logger.info(f"Execution time: {end_time-start_time} seconds")

if __name__ == '__main__':
    main()
