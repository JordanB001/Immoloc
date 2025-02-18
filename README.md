# Getting started

## Requirements

- any Debian based system (Debian, Ubuntu)
- Python version between 3.9 and 3.12.9

- curl
- unzip
- python[YOUR_PYTHON_VERSION]-venv

## Installation

Just follow these commands:

```` bash
curl -L -o immoloc-back.zip https://github.com/JordanB001/Immoloc-Back/archive/refs/heads/main.zip
unzip immoloc-back.zip
rm immoloc-back.zip
cd Immoloc-Back-main

python -m venv venv
. venv/bin/activate
pip install -r requirement.txt
````

Create `.env` and fill it with your secret key and API key:

```` bash
nano .env
````

`example.env`:

``` text
SECRET_KEY=<your_secret_key>
API_KEY=<your_api_key>
```

## Launching

## manually

```` bash
gunicorn --reload --bind=0.0.0.0 'immoloc:create_app()'
````

### as system service

add the service : (this example is with user root)

```` bash
nano /etc/systemd/system/immoloc.service
````

```` bash
[Unit]
Description=Flask Application Service
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root
ExecStart=/root/venv/bin/gunicorn --reload --bind=0.0.0.0 'immoloc:create_app()'
Restart=always
RestartSec=3
Environment=PYTHONPATH=/root

[Install]
WantedBy=multi-user.target
````

Check if the api is running with :

```` bash
systemctl status immoloc_api.service
````

## API

## Endpoints

### 1. Analyze a real estate ad

URL: "/analyze"
Method: POST
Body: json

``` json
{
    "real_estate_ad": "your real estate ad description"
}
```

Example:

``` json
{
    "real_estate_ad": "House for sale, 5 rooms, 2 bedrooms, in Moyen (54118). Discover without delay, this house of about 100 m²."
}
```

Response:

``` json
{
    "real_estate_ad": "This real estate sale ad presents a house of 100 m² located in Moyen (54118), comprising 5 rooms including 2 bedrooms. Here is a critical analysis of this ad:
    1. Location: Mentioning the location in Moyen (54118) is a good point, as it allows potential buyers to geographically locate the property. However, it would be useful to add information about the specific neighborhood or nearby amenities (schools, transport, shops, etc.) to give a better idea of the environment."
}
```

### 2. Estimate the price and range of a real estate ad

URL: "/estimate"
Method: POST
Body: json

``` json
{
    "real_estate_ad": "your real estate ad description with location, surface, and type of property"
}
```

Example:

``` json
{
    "real_estate_ad": "city Lyon, surface 50m², apartment"
}
```

Response:

``` json
{
    "average_price": 950,
    "min_range": 900,
    "max_range": 1000
}
```

### 3. Generate a beautiful real estate ad from a description

URL: "/generate"
Method: POST
Body: json

``` json
{
    "real_estate_ad": "your real estate ad description"
}
```

Example:

``` json
{
    "real_estate_ad": "House for sale, 5 rooms, 2 bedrooms, in Moyen (54118). 100 m², land 363m2, 40000 euros, ground floor: kitchen, dining room, living room. 1st floor: 2 bedrooms. attic"
}
```

Response:

``` json
{
    "real_estate_ad": "Discover without delay, this house of about 100 m², to be completely renovated, offers a great opportunity for project lovers. Located in a quiet area and close to amenities, it has all the assets to become your future home.
    Property description:
    Ground floor: A kitchen, a dining room, and a bright living room, perfect for creating a friendly living space.
    1st floor: Two spacious bedrooms ready to be modernized.
    Convertible attic: Give yourself the possibility to add additional rooms or a leisure space.
    Outbuildings: A garage and annexes for storage or other projects.
    Non-adjoining land: About 360 m² nearby, ideal for a garden, a vegetable garden, or a relaxation area.
    Technical elements: Roof in good condition and PVC double-glazed windows.
    Why choose this house?
    With its spaces to renovate and its convertible attic, this house is a blank canvas to realize your ideas. Its non-adjoining land and quiet environment add extra charm."
}
```

## Known HTTP Errors

```text
400 Bad Request: Input data is malformed.
500 Internal Server Error: General server error or database issues.
```
