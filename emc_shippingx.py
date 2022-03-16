import requests
import json
import platform
import subprocess
import os
import tarfile
from fabric import Connection
from dotenv import load_dotenv
load_dotenv()

def get_xi_data(url):
    response = requests.get(url)
    data = json.loads(response.text)
    data = data[0]['fields']
    return data


""" 
* sends SMS alerts
* @params url, params
* return dict
"""


def alert(url, params):
    headers = {'Content-type': 'application/json; charset=utf-8'}
    r = requests.post(url, json=params, headers=headers)
    return r

recipients = ["+26599589034411"]
recipients = ["+26599827671211"]
cluster = get_xi_data('http://10.44.0.52/sites/api/v1/get_single_cluster/1')

for site_id in cluster['site']:
    site = get_xi_data('http://10.44.0.52/sites/api/v1/get_single_site/' + str(site_id))

    # functionality for ping re-tries
    count = 0

    while (count < 3):

        # lets check if the site is available
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        if subprocess.call(['ping', param, '1', site['ip_address']]) == 0:
              
            # ship iBLIS to remote site
            push_emc = "rsync " + "-r $WORKSPACE/emastercard-upgrade-automation/tmp/emastercard-upgrade-automation.tgz "+ site['username'] + "@" + site[
                'ip_address'] + ":/var/www"
            os.system(push_emc)
                
            
            push_emc_script = "rsync " + "-r $WORKSPACE/emc_setup.sh  "+ site['username'] + "@" + site[
                'ip_address'] + ":/var/www/"
            os.system(push_emc_script)
            
            run_emc_script = "ssh " + site['username'] + "@" + site['ip_address'] + " 'cd /var/www/ && ./emc_setup.sh'"
            os.system(run_emc_script)
            
          
            # send sms alert
            for recipient in recipients:
                msg = "Hi there,\n\nDeployment of iBlis to " + site['name'] + " completed succesfully.\n\nThanks!\nEGPAF HIS."
                params = {
                    "api_key": os.getenv('API_KEY'),
                    "recipient": recipient,
                    "message": msg
                }
                alert("http://sms-api.hismalawi.org/v1/sms/send", params)

            count = 3
        else:
            count = count + 1

            # make sure we are sending the alert at the last pint attempt
            if count == 3:
                for recipient in recipients:
                    msg = "Hi there,\n\nDeployment of iBlis for " + site['name'] + " failed to complete after several connection attempts.\n\nThanks!\nEGPAF HIS."
                    params = {
                        "api_key": os.getenv('API_KEY'),
                        "recipient": recipient,
                        "message": msg
                    }
                    alert("http://sms-api.hismalawi.org/v1/sms/send", params)
