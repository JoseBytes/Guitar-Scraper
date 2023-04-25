[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python Version](https://img.shields.io/badge/python-%3E%3D%203.7-blue.svg)


# Guitar Scraper

This Python script allows you to extract guitar information and save it to a CSV file or enter the information from Google Sheets.

## Requirements

 - Python >= 3.7
 - Libraries: **requests, BeautifulSoup, pandas, tqdm**
 - In case of using the Script with the Google Sheets API:
   **google-auth, google-auth-oauthlib, google-auth-httplib2**

## Facility

1. Clone this repository or download the ZIP file.
2. Install the necessary libraries with the following command:
**`> pip install -r requirements.txt`**
4. In case of using the script with Google Sheets API, execute the command:
 **`> pip install google-auth==1.28.0 google-auth-oauthlib==0.4.4 google-auth-httplib2==0.4.1`**

## Use

1. Run the script with the following command:
**`> python <name.py>`**
Example:
**`> python guitarKitWorld-csv.py`**
3. Wait for the script to finish extracting all the information.
4. Verify that the **`guitarKitWorld.csv`** file has been created in the same directory.

## Result

The script generates a CSV file with the following information for each guitar found on the web page:

| URL | Image URL | Title | Hand Orientation | Neck Joint | Neck Material | Neck Nut Material | Fretboard Material | Number of Frets | Scale Length | Body Type | Body Material | Pickup | Pickguard | Hardware Set Finish | Prices |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| https://..... | https://..... | T-Style 12-String | Right Handed | Bolt-On | maples | Bone | maples | 21 | 25.5" | Solid Body | Basswood | S-S | None | Chrome | $299.00 |

While the information is being scraped from each site, the extracted images are downloaded with the name of the product.

![App Screenshot](https://github.com/JoseBytes/Guitar-Scraper/blob/main/img/result_download.png)

## Information

This script was developed by [Jose Lujan](https://github.com/JoseBytes).
