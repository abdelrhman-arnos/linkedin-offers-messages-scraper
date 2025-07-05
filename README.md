# LinkedIn Offers Messages Scraper

This project automates the extraction of LinkedIn message threads that contain job offers or related keywords using Selenium WebDriver. The extracted messages are saved to a CSV file for further analysis.

## Features

- Logs into LinkedIn using your credentials.
- Scans all message threads for keywords such as "offer", "salary", "rate", "contract", "position", "remote", "opportunity", "full-time", and "part-time".
- Extracts sender, date, and message content for relevant messages.
- Saves the results to `linkedin_offers.csv`.

## Requirements

- Python 3.7+
- Google Chrome browser
- [ChromeDriver](https://developer.chrome.com/docs/chromedriver/downloads) (compatible with your Chrome version)

## Installation

1. Clone this repository:
    ```cmd
    git clone <repo-url>
    cd linkedin_offers_messages
    ```

2. Install dependencies:
    ```cmd
    pip install -r requirements.txt
    ```

3. Copy `.env.example` to `.env` and set your LinkedIn credentials:
    - `LINKEDIN_USERNAME` (your LinkedIn email or username)
    - `LINKEDIN_PASSWORD` (your LinkedIn password)

    Example:
    ```cmd
    copy .env.example .env
    # Then edit .env to add your credentials
    ```

## Usage

1. Make sure ChromeDriver is installed and in your PATH.
2. Run the script:
    ```cmd
    python main.py
    ```
3. After completion, check the generated `linkedin_offers.csv` file for the extracted messages.

## Notes

- This script uses Selenium to automate browser actions. Make sure you comply with LinkedIn's terms of service.
- For best results, do not use your main LinkedIn account.
- You may need to update ChromeDriver if your Chrome browser updates.

## License

This project is for educational