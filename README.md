# Webscraper

The set of scripts allow to scrape job information from the different freelancer platforms based on keywords.  
Currently, the following platforms are supported:  
- [freelancer.com](https://www.freelancer.com/jobs/regions/)  
- [upwork.com](https://www.upwork.com/)  

The project is designed with Selenium WebDriver(Selene) + Pytest + PageObject pattern.
The results might be saved into csv/xlsx files or send as a slack notification. 

## Requirements

Run `pip install -r requirements.txt`  
Make sure Google Chrome Driver, Mozilla GeckoDriver or PhantomJS are available on your $PATH (or %PATH% on Windows)  
For slack notification add `SLACK_TOKEN` to environment variables with correct value  

## Usage

Run from the project directory `pytest`  

## Project Goals

The code is written for educational purposes only.
