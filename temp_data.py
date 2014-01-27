""" Example subclass on ninja.devices.TemperatureSensor and runner.

Convenience features:
- Set timezone offset
- Verbosity controls whether to print after each poll or only when the value has changed since the last poll
- Set tz offset, pulse_interval, and verbosity from command-line arguments
"""

from ninja.devices import TemperatureSensor
from datetime import timedelta

from setup import *
from auth import TEMPERATURE_LOGGING_GUID

SENSOR_GUID = TEMPERATURE_LOGGING_GUID


class MyTemperatureSensor(TemperatureSensor):
    pulse_interval = 10
    verbose_print = True
    tz_offset = 0
    _last_data = None

    def print_data(self, inst, data):
        # Get the datetime value with specified timezone offset
        last_read = inst.last_read - timedelta(hours=self.tz_offset)

        # Calculate the change between this and last print
        delta = data.f - self._last_data if self._last_data is not None else None

        # Print the data if appropriate
        if self.verbose_print is True or self._last_data != data.f:
            print '%s : %s %s' % (last_read, data.f, 'Change: %s' % delta if delta is not None else '')

        # Update current record of temperature data
        self._last_data = data.f

    def pulse(self, period=pulse_interval):
        run_pulse = True
        while run_pulse is True:
            try:
                super(MyTemperatureSensor, self).pulse(self.pulse_interval)
            except KeyboardInterrupt:
                run_pulse = False
        print ''


def get_parsed_arguments():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v',
        '--verbose',
        help='Turns on verbose printing, else only prints on change',
        action='store_true'
    )
    parser.add_argument(
        '-i',
        '--interval',
        type=int,
        help='Sets the pulse interval (in seconds)',
        default=10
    )
    parser.add_argument(
        '-tz',
        '--timezone',
        type=int,
        help='Timezone offset to apply to printed datetime values',
        default=0
    )
    args = parser.parse_args()
    return args.verbose, args.interval, args.timezone


temp_sensor = MyTemperatureSensor(api, SENSOR_GUID)

if __name__ == '__main__':
    temp_sensor.verbose_print, temp_sensor.pulse_interval, temp_sensor.tz_offset = get_parsed_arguments()
    temp_sensor.onHeartbeat(temp_sensor.print_data)
    temp_sensor.pulse()
