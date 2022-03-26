# Microcenter GPUs scraper

A very simple web scraper that extracts the currently listed GPUs for sale in Microcenter. It is implemented in Python and
uses the scrapy library.

## Installing Scrapy

This scraper requires python 3.6+, pip and scrapy with its additional dependencies.

### Creating virtual enviroment (Optional)

Creation of virtual environments is done using the command venv

`python -m venv .venv`

Activate the virtual enviroment

`.venv\scripts\activate.bat`

Install the dependencies (scrapy)

`pip3 install scrapy`

After this you're good for excecution

### Installing Scrapy globally

If you want to install Scrapy in the whole system you only need to excetute this command

`pip3 install scrapy`

## Excecution

Once you have installed Scrapy succesfully you need to execute the following command 
inside the project folder (gpu_scrapper)

`scrapy crawl gpu`

Or you can also run the following `sh` script

`./run.sh`

## Save the output file in CSV

For saving the scraped result in a CSV file run the following command

`scrapy crawl gpu -o _filename_.csv`

Or you can also run the following `sh` script

`./save.sh`

NOTE: This was made for an assignment in the Costa Rica Institute of Technology