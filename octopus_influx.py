import pandas as pd
import os
import logging
from dateutil.parser import isoparse
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from octopus_energy_client import OctopusEnergy, ResourceType

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("octopus-influx.log"),
        logging.StreamHandler()
    ]
)

class OctopusInflux:
    """
    Facilitates importing of Octopus Energy consumption data into an Influx Db bucket.
    """
    dry_run = False

    def __init__(self,
        influx_db_url=None,
        influx_api_token=None,
        influx_organisation=None,
        influx_bucket=None,
        octopus_api_key=None, 
        octopus_electricity_serial=None,
        octopus_electricity_mpan=None,
        octopus_gas_serial=None,
        octopus_gas_mprn=None,
        dry_run=False):

        self.dry_run=dry_run
        self.influx_db_url = influx_db_url or os.environ["INFLUX_DB_URL"]
        self.influx_db_token = influx_api_token or os.environ["INFLUX_DB_TOKEN"]
        self.influx_db_org = influx_organisation or os.environ["INFLUX_DB_ORG"]
        self.influx_db_bucket = influx_bucket or os.environ["INFLUX_DB_BUCKET"]

        self.octopus_client = OctopusEnergy(
            api_key=octopus_api_key,
            electricity_serial=octopus_electricity_serial,
            electricity_mpan=octopus_electricity_mpan,
            gas_serial=octopus_gas_serial,
            gas_mprn=octopus_gas_mprn
        )

    def resource_to_influx(self, resource, consumption, serial, units, date_from):
        if consumption.get("count") == 0:
            logger.warn(f"No {resource} consumption data is available for {serial} on {date_from:%Y-%m-%d}")
            return

        with InfluxDBClient(url=self.influx_db_url, token=self.influx_db_token, org=self.influx_db_org) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            day_total = 0.0

            for result in consumption.get('results'):
                consumption = float(result.get('consumption', 0))
                day_total += consumption
                start = isoparse(result.get('interval_start'))
                end = isoparse(result.get('interval_end'))

                logger.info(f"{resource} consumption for period: {start} - {end} = {consumption}{units}")

                point = Point("consumption_half_hourly") \
                    .tag("resource", resource) \
                    .tag("serial", serial) \
                    .tag("units", units) \
                    .field("value", consumption) \
                    .time(end, WritePrecision.NS)

                if not self.dry_run:
                    logger.debug("Writing half-hourly data to influx")
                    write_api.write(self.influx_db_bucket, self.influx_db_org, point)

            logger.info(f"{resource} consumption total for {date_from:%Y-%m-%d}: {day_total}{units}")

            point = Point("consumption_daily") \
                .tag("resource", resource) \
                .tag("serial", serial) \
                .tag("units", units) \
                .field("value", day_total) \
                .time(date_from, WritePrecision.NS)

            if not self.dry_run:
                logger.debug("Writing daily data to influx")
                write_api.write(self.influx_db_bucket, self.influx_db_org, point)

    def electricity_to_influx(self, date_from):        
        self.resource_to_influx(
            "electricity",
            self.octopus_client.get_consumption_for_date(ResourceType.ELECTRICITY, date_from),
            self.octopus_client.octopus_electricity_serial,
            self.octopus_client.electricity_consumption_units,
            date_from
        )
    
    def gas_to_influx(self, date_from):
        self.resource_to_influx(
            "gas",
            self.octopus_client.get_consumption_for_date(ResourceType.GAS, date_from),
            self.octopus_client.octopus_gas_serial,
            self.octopus_client.gas_consumption_units,
            date_from
        )

    def run_date(self, date_from):
        logger.info(f"Running for date: {date_from}")
        self.electricity_to_influx(date_from)
        self.gas_to_influx(date_from)

    def run_dates(self, dates):
        for date_from in dates:
            self.run_date(date_from)
    