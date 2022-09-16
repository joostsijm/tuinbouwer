"""Main app"""

import sys
import time

from tuinbouwer_server_api import create_app


def main():
    """Main application"""
    app = create_app()
    app.run()
    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()
