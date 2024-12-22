from app.app import create_app
import logging

app = create_app()
if __name__ == '__main__':
    # logging.info('info的体质')
    # logging.debug('de bug日志')
    app.run()

