# Octopus Influx

Imports Octopus Energy consumption data into an Influx Db.

See [https://developer.octopus.energy/docs/api/](https://developer.octopus.energy/docs/api/) for more details of the Octopus API.

## Usage

```shell
chmod +x octopus_influx
./octopus_influx --help

usage: octopus_influx [-h] [--dates 2022-01-15 [2022-01-15 ...]] [--apikey sk_live_xxxxxxxxxxxxx] [--elecserial 01J0123456] [--mpan 0123456789012] [--gasserial A1B00123456789] [--mprn 123456789] [--influxdb http://localhost:8086] [--token xxxxxxxxxxxxxxxxXXXXXXXxxxxxx==] [--org myOrg] [--bucket myBucket] [--dryrun]

Import octopus energy consumption data to InfluxDb.

optional arguments:
  -h, --help            show this help message and exit
  --dates 2022-01-15 [2022-01-15 ...]
                        Dates to run
  --dryrun              Enable Dry Run Mode - data is not published to influx

Octopus Energy:
  Octopus Energy API inputs. Any not specified will be taken from environment variables.

  --apikey sk_live_xxxxxxxxxxxxx
                        Octopus API Key. If blank, environment variable OCTOPUS_API_KEY is used
  --elecserial 01J0123456
                        Octopus Electricity Meter Serial Number. If blank, environment variable OCTOPUS_ELECTRICITY_SERIAL is used
  --mpan 0123456789012  Octopus Electricity MPAN. If blank, environment variable OCTOPUS_ELECTRICITY_MPAN is used
  --gasserial A1B00123456789
                        Octopus Gas Meter Serial Number. If blank, environment variable OCTOPUS_GAS_SERIAL is used
  --mprn 123456789      Octopus Gas MPRN. If blank, environment variable OCTOPUS_GAS_MPRN is used

Influx Db:
  Influx Db API inputs. Any not specified will be taken from enironment variables.

  --influxdb http://localhost:8086
                        Influx Database URL. If blank, environment variable INFLUX_DB_URL is used
  --token xxxxxxxxxxxxxxxxXXXXXXXxxxxxx==
                        Influx API Token. If blank, environment variable INFLUX_DB_TOKEN is used
  --org myOrg           Influx Organisation Name. If blank, environment variable INFLUX_DB_ORG is used
  --bucket myBucket     Influx Bucket Name. If blank, environment variable INFLUX_DB_BUCKET is used

Example: octopus_influx --dates 2022-01-15
```

## Environment Variables

The script will use the following environment variables in place of arguments:

* OCTOPUS_API_KEY
* OCTOPUS_ELECTRICITY_MPAN
* OCTOPUS_ELECTRICITY_SERIAL
* OCTOPUS_GAS_MPRN
* OCTOPUS_GAS_SERIAL
* INFLUX_DB_URL
* INFLUX_DB_TOKEN
* INFLUX_DB_ORG
* INFLUX_DB_BUCKET

## Influx Db Setup

See [https://docs.influxdata.com/influxdb/v2.0/install/](https://docs.influxdata.com/influxdb/v2.0/install/)
