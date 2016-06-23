import argparse, sys, os

###############################################################################
#                           argparse configuration                            #
###############################################################################

parser = argparse.ArgumentParser(description='CERN HLoader')

parser.add_argument('-c', '--check-sanity', action='store_true', help='Check the sanity of the execution environment')
parser.add_argument('-r', '--run', help='Run the Flask microserver', action='store_true')
parser.add_argument('--debug', help='Enable debugging mode', action='store_true', default=False)
parser.add_argument('--use-reloader', action='store_true', help='Use reloader to run Flask microserver', default=False)
parser.add_argument('--config-file', action='store', help='Specify the path to the configuration file', default=[os.path.dirname(os.path.abspath(__file__))+'/hloader/config/config.ini'])

args = vars(parser.parse_args())

if args['check_sanity']:
        pass

if args['run']:
    os.environ["HL_CONFIG_FILE"] = str(args['config_file'])

    from hloader.config import config
    from hloader.db.DatabaseManager import DatabaseManager
    from hloader.backend.api import app  # initialize the application in hloader.backend.api

    if not (config.POSTGRE_ADDRESS and
            config.POSTGRE_PORT and
            config.POSTGRE_USERNAME and
            config.POSTGRE_PASSWORD and
            config.POSTGRE_DATABASE):
        raise Exception("Config not properly set up.")

    DatabaseManager.connect_meta("PostgreSQLA",
                                 config.POSTGRE_ADDRESS,
                                 config.POSTGRE_PORT,
                                 config.POSTGRE_USERNAME,
                                 config.POSTGRE_PASSWORD,
                                 config.POSTGRE_DATABASE)

    DatabaseManager.connect_auth(config.AUTH_ADDRESS,
                                 config.AUTH_PORT,
                                 config.AUTH_USERNAME,
                                 config.AUTH_PASSWORD,
                                 config.AUTH_SERVICE_NAME)

    if __name__ == "__main__":
        app.run(debug=args['debug'], use_reloader=args['use_reloader'])

    views.__author__  # placeholder, so the views initializer script won't get deleted by accidental auto-formatting
