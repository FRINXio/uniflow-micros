import time
import worker_wrapper
from frinx_rest import conductor_url_base, conductor_headers
import cli_worker
import netconf_worker
import uniconfig_worker
import common_worker
import http_worker
import os
import requests

workflows_folder_path = './workflows'
workflow_import_url = conductor_url_base + '/metadata/workflow'


def main():
    print('Starting FRINX workers')
    cc = worker_wrapper.ExceptionHandlingConductorWrapper(conductor_url_base, 1, 1)
    register_workers(cc)
    import_workflows(workflows_folder_path)



    # block
    while 1:
        time.sleep(1000)


def register_workers(cc):
    cli_worker.start(cc)
    netconf_worker.start(cc)
    uniconfig_worker.start(cc)
    common_worker.start(cc)
    http_worker.start(cc)


def import_workflows(path):
    if os.path.isdir(path):
        print("\nIt is a directory")
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_file():
                    try:
                        print('Importing workflow ' + entry.name)
                        with open(entry, 'rb') as payload:
                            r = requests.post(workflow_import_url,
                                              data=payload, headers=conductor_headers)
                    except Exception as err:
                        print('Error while registering task ' + traceback.format_exc())
                        raise err
                elif entry.is_dir():
                    import_workflows(entry.path)
                else:
                    print(entry)
    else:
        print("Path not a directory")


if __name__ == '__main__':
    main()
