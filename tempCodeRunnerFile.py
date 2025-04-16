chrome_options = Options()

# Setup WebDriver with updated service
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)