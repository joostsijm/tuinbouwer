"""Main app"""

import sys
import time

from tuinbouwer_sensor import SCHEDULER, LOGGER, jobs


def main():
    """Main method"""
    # jobs.send_log_information()

    LOGGER.info('Starting application')
    SCHEDULER.add_job(
        jobs.send_log_information,
        'cron',
        id='job_send_log_information',
        replace_existing=True,
        # minute='0,10,20,30,40,50'
        minute='0,5,10,15,20,25,30,35,40,45,50,55'
    )

    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        LOGGER.info('Exiting application')
        SCHEDULER.shutdown()
        sys.exit()

if __name__ == '__main__':
    main()
