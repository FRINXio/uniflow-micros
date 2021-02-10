import time
import worker_wrapper
from frinx_rest import conductor_url_base, conductor_headers
import cli_worker
import netconf_worker
import uniconfig_worker
import common_worker
import http_worker
from import_workflows import import_workflows
import requests
import flask

workflows_folder_path = '../workflows'

app = flask.Flask(__name__)
cc = None


@app.route('/api/readiness', methods=['GET'])
def readinessCheck():
    # worker_wrapper check
    if not checkMyself():
        flask.abort('Internal error')
    # conductor server check
    conductor_status = checkConductorConnection()
    if 199 < conductor_status < 300:
        return str(conductor_status)
    else:
        flask.abort(conductor_status)


def checkConductorConnection():
    try:
        return requests.get(conductor_url_base + '/health').status_code
    except requests.exceptions.RequestException as err:
        print("Something is wrong:", err)
        return flask.abort(err)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        return flask.abort(errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        return flask.abort(errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        return flask.abort(errt)


def checkMyself():
    try:
        if cc.timestamp:
            return True
        else:
            return False
    except ...:
        return False


def main():
    print('Starting FRINX workers')
    global cc
    cc = worker_wrapper.ExceptionHandlingConductorWrapper(conductor_url_base, 1, 1)
    register_workers(cc)
    import_workflows(workflows_folder_path)

    app.run(port=5005)


def register_workers(cc):
    cli_worker.start(cc)
    netconf_worker.start(cc)
    uniconfig_worker.start(cc)
    common_worker.start(cc)
    http_worker.start(cc)


if __name__ == '__main__':
    main()
