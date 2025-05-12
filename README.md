# JADN ISO 3166 Country and Subdivisions

* `chromedriver.exe`: WebDriver downloaded for Browser and Platform, e.g.,
[Chrome](https://sites.google.com/chromium.org/driver/getting-started)
* `get-iso3166.py`:
Download information from ISO [Online Browsing Platform](https://www.iso.org/obp/ui/#search),
save in [JSON format](json) to avoid costly and slow server access.
* `make-iso3166-jadn.py`:
Convert the saved JSON data to JADN packages for IS0 3166-1 country codes and
3166-2 subdivision codes for each country.