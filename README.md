# Technical Exercise

## Specification
- Python Version: 3.12
- IDE: PyCharm
- OS: MacOS

## Overview
Settlement system prices by settlement date (DISEBSP)

The aim of this project is to create a daily report to support a trader’s post-trade analysis based on information collected 
from Elexon Insights (BMRS) API regarding system imbalance price and previous settlement day's cost.

- Documentation: https://bmrs.elexon.co.uk/api-documentation/introduction
- Endpoint: https://bmrs.elexon.co.uk/api-documentation/endpoint/balancing/settlement/system-prices/%7BsettlementDate%7D


| Field                                   | Type           | Definition                                                                                                                                                                                                                                           |
|-----------------------------------------|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `settlementDate`                        | Date           | The settlement date for the balancing market period (YYYY-MM-DD).                                                                                                                                                                                    |
| `settlementPeriod`                      | Integer        | The settlement period within the settlement date. Typically 48 half-hour settlement periods per day (or 46/50 during daylight saving).                                                                                                               |
| `startTime`                             | DateTime (UTC) | Timestamp marking the start of the settlement period.                                                                                                                                                                                                |
| `createdDateTime`                       | DateTime (UTC) | Timestamp when this settlement price record was created or published.                                                                                                                                                                                |
| `systemSellPrice (SSP)`                 | Float          | Represents the price paid to market participants that are long (have excess energy) during the settlement period.                                                                                                                                    |
| `systemBuyPrice (SBP)`                  | Float          | Represents the price charged to market participants that are short (have insufficient energy) during the settlement period.                                                                                                                          |
| `bsadDefaulted`                         | Boolean        | Indicates whether the Balancing Services Adjustment Data (BSAD) used default values (`true`) or actual calculated values (`false`).                                                                                                                  |
| `priceDerivationCode`                   | String / Null  | Code indicating how the imbalance price was derived (for example, calculated normally or via an alternative pricing methodology).                                                                                                                    |
| `reserveScarcityPrice`                  | Float / Null   | Additional scarcity price applied when reserve shortages exist. A value of `0` indicates no reserve scarcity adjustment.                                                                                                                             |
| `netImbalanceVolume (NIV)`              | Float          | Net volume of energy that the system operator (SO) needs to buy or sell to balance the electricity system during the settlement period (MWh). Positive values indicate a short system; negative values indicate a long system; 0 indicates balanced. |
| `sellPriceAdjustment`                   | Float / Null   | Any adjustment applied to the System Sell Price.                                                                                                                                                                                                     |
| `buyPriceAdjustment`                    | Float / Null   | Any adjustment applied to the System Buy Price.                                                                                                                                                                                                      |
| `replacementPrice`                      | Float / Null   | Used if the standard imbalance price could not be calculated. `null` indicates no replacement price was required.                                                                                                                                    |
| `replacementPriceReferenceVolume`       | Float / Null   | The reference volume associated with the replacement price calculation. `null` if no replacement price was used.                                                                                                                                     |
| `totalAcceptedOfferVolume`              | Float / Null   | Total volume of accepted offers in the balancing mechanism during the settlement period (MWh).                                                                                                                                                       |
| `totalAcceptedBidVolume`                | Float / Null   | Total volume of accepted bids in the balancing mechanism during the settlement period (MWh). Typically negative to indicate downward balancing actions.                                                                                              |
| `totalAdjustmentSellVolume`             | Float / Null   | Represents system-wide volume of energy—measured in Megawatt-hours (MWh) — that the system operator accepted to reduce generation or increase demand (a 'sell' action) during a specific Settlement Period.                                          |
| `totalAdjustmentBuyVolume`              | Float / Null   | Represents system-wide volume of energy—measured in Megawatt-hours (MWh) — that the system operator accepted to increase generation or reduce demand (a 'buy' action) during a specific Settlement Period.                                           |
| `totalSystemTaggedAcceptedOfferVolume`  | Float / Null   | Total accepted offer volume remaining after system tagging, which removes actions not considered system-related for pricing purposes (MWh).                                                                                                          |
| `totalSystemTaggedAcceptedBidVolume`    | Float / Null   | Total accepted bid volume remaining after system tagging (MWh).                                                                                                                                                                                      |
| `totalSystemTaggedAdjustmentSellVolume` | Float / Null   | System-tagged adjustment volume applied to sell actions. May be `null` if no adjustment exists.                                                                                                                                                      |
| `totalSystemTaggedAdjustmentBuyVolume`  | Float / Null   | System-tagged adjustment volume applied to buy actions (MWh).                                                                                                                                                                                        |


## Structure of application
```
IndicativeImbalanceSettlement/
│
├── src/
│   └── apps/                                         # Applications Folder
│       └── imbalance_settlement/                     # ELEXON DISEBSP APIs Folder 
│           ├── configs/                              # Configurations per API
│           │   └── settlement_system_prices/
│           │       └── configuration.py
│           ├── core/                                 # Business logic
│           │   └── settlement_system_prices/
│           │       ├── app.py
│           │       ├── time_series.py
│           │       └── visualisation.py
│           ├── logs/                                 # .log files containing logging messages
│           ├── tests/                                # Tests including Unit Test
│           │   └── settlement_system_prices/
│           │       ├── test_core/
│           │       └── test_utils/
│           ├── utils/                                # Shared Resources e.g. Functions/ Classes
│           │   ├── api.py
│           │   ├── constants.py
│           │   ├── exceptions.py
│           │   ├── log.py
│           │   ├── schema.py
│           │   ├── util.py
│           │   └── validate.py
│           └── main.py                               # Entrypoint to application                              
│
├── .gitignore                                        # Untracked folders/ files
├── pyproject.toml                                    # Contains config for pytest-cov
├── README.md                                         # Application instructions
├── requirements.txt                                  # Prod Application Dependencies
└── requirements-dev.txt                              # Dev Application Dependencies
```

## Key assumptions and trade-offs
1. I have assumed that there are no payload duplicate data where settlement periods are different and the rest of the data is the same.
e.g. {"settlementPeriod": 2, "systemSellPrice": 215, "systemBuyPrice": 215, bsadDefaulted": false} and 
{"settlementPeriod": 3, "systemSellPrice": 215, "systemBuyPrice": 215, bsadDefaulted": false}
2. Only 'json' format is supported for incoming API data. Other formats like csv and xml are not supported.
3. If other APIs were to be added, I have assumed BASE_URL and HEADERS will remain the same.
4. Data has been validated line by line during processing instead of carrying out two processes (data validation and processing).
The reason for this is that it would double the number of operations performed. Additionally, because the operation has 
an O(n) time complexity, the execution time may also approximately double as the input size increases.
However, since the size of payload data is small, the speed difference would be negligible. I have also assumed 
that Elexon mostly provides correct data and that there error rates are low. If the error rates were to be high, then it
might be best to validate the data first.
5. I have only validated the data that is relevant from the API. Usually any incoming raw data is stored in data lakes
and then transformed into clean data. This clean data is stored in data warehouses before being used for analytics or 
reporting purposes.
6. I have assumed that the data will always be small. But tested validation below to see how it would perform if schema 
was used to process large size of data.

| Number of Dict Items in API `data` section | `dataclasses.dataclass`  | `pydantic.dataclasses.dataclass`  |
|--------------------------------------------|--------------------------|-----------------------------------|
| 1                                          | 0.000000420              | 0.000000391                       |
| 100                                        | 0.000023310              | 0.000022300                       |
| 1,000                                      | 0.000138500              | 0.000116400                       |
| 1,00,000                                   | 0.013823221              | 0.012187000                       |
| 1,000,000                                  | 0.141668000              | 0.128066243                       |

## Additional Steps (with more time)
1. With more time, a strategy pattern can perhaps be implemented for different format types as we can interchange 
between csv, xml and json api data.
2. get_logger function in log.py file can be written as a class and extended further.
3. More tests can be written including end-to-end test and tests for different api headers and param formats. Further 
improvements can be made in terms of using fake data for testing. Faker python library could perhaps be used.

## Notes
1. Data can only be fetched from 2015-11-06. Prior to this date, there is no data.
2. SSP/SBP prices can be negative. Approx 99.7% of the data is positive. Data was checked.

## Chart Explanation
1. niv_price_bar_line_plot -> This chart enables traders with quick post-analysis and helps identify potential anomalies 
like any repetition or inverse relationships. For example, this particular chart (imbalance_analysis_20260713_195124.png) 
shows at least 3 anomalies that traders can investigate:
- NIV was positive at approximately 3pm within a 12-hour period from 6:30am to 5pm. 
- Price was highest at the very start of the day at 12:00am, but not volume. 
- There are 4 periods in total where price was inversely correlated with NIV. One could question whether this happens 
on a daily basis and at what time.
2. niv_price_scatter_plot -> This chart shows shape and steepness of the NIV and System Price relationship. For example,
it shows us how much price responds per MWh of imbalance. Some of the anomalies traders can investigate are:
- Gap between £10 and £50
- Detect any clusters to understand what price and volume range they usually occur within.

## Running the Application
1. Clone the repository ```git clone <repository>``` into a folder.
2. Create a virtual environment
```
WINDOWS
python -m venv venv
venv\Scripts\activate

MACOS
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies (for prod): ```pip install -r requirements.txt ```. Otherwise ```pip install -r requirements-dev.txt ``` for dev.
4. Run the application via CLI: ```python -m src.apps.imbalance_settlement.main```

## Running Unit Tests
This project uses pytest for testing.

1. To run all tests: ```pytest```
2. To run a specific test file e.g. 
```pytest src/apps/imbalance_settlement/tests/test_imbalance_settlement/test_utils/test_util.py```

## Troubleshooting
1. Use PYTHONPATH to set path to 'src' folder (if need be).
