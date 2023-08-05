import requests
from flask import Flask, request

app = Flask(__name__)

def applicationNumExtract1(PatNum):
    url = 'https://patentcenter.uspto.gov/retrieval/public/v2/application/data'
    params = {'patentNumber': PatNum}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, params=params, headers=headers)
    #print(response.content)
    if response.status_code == 200:
        json_data = response.json()
        application_number_text = json_data["applicationMetaData"]["applicationIdentification"]["applicationNumberText"]
        # Trim the AppNumberText and return it
        modified_app_number_text = application_number_text.strip()
        return modified_app_number_text

def LegalStatusExtract(PatNum, AppNumberText):
    url = "https://fees.uspto.gov/mntfee-services/v1/maintenancefee/details"
    params = {'patentNumber': PatNum, 'applicationNumber': AppNumberText}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, params=params, headers=headers)
    res = response.content.decode('utf-8')
    print(res)
    if response.status_code == 200:
        data = response.json()
        x=data['infoMessageText'][0]
        return x

@app.route('/feeInfo', methods=['GET'])
def feeInfo():
    patentNumber = request.args.get('patentNumber')
    modified_patent_number = patentNumber[2:-2]
    # Get the trimmed AppNumberText
    AppNumnberText = applicationNumExtract1(modified_patent_number)
    x = LegalStatusExtract(modified_patent_number, AppNumnberText)
    return x

if __name__ == '__main__':
    app.run(debug=True)
