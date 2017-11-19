from azure.storage.blob import BlockBlobService

azure_storage_account_name = 'med'
azure_storage_account_key = 'gAhZS9iD56r3fRN+/lokQSE4CAysWtuqc5H2xSeCb9GLJdmS4FEBrUIqYHuj/RdiqOK+haJva2u7A6OkrLUzOg=='

if azure_storage_account_name is None:
    raise Exception("You must provide a name for an Azure Storage account")

api_key = 'd10d6e5ff2aa413e8f39ba1aa2ae241e'

# create blob service object to access the files in the storage
# You can access your account_name and account_key values at [Azure Management Portal](https://portal.azure.com)
blob_service = BlockBlobService(azure_storage_account_name, azure_storage_account_key)

# select container (folder) name where the files resides
container_name = 'blood'

# # list files in the selected folder
# generator = blob_service.list_blobs(container_name)
#
# blob_prefix = 'https://{0}.blob.core.windows.net/{1}/{2}'
#
# img_list = []
#
# print("List of files in the container:")
# for blob in generator:
#     url = (blob_prefix.format(blob_service.account_name, container_name, blob.name))
#     print (url)
#     img_list.append(blob.name)
#
# len(img_list)


img_url = blob_prefix.format(blob_service.account_name, container_name, img_list[6])

# img_url = 'blob:https://web.telegram.org/91e3f998-9236-4056-b92d-9edc8c636efe'

img = ipImage(url=img_url, width=250, height=250)


from PIL import Image
import io
import httplib, urllib, base64
# import cStringIO

# image_file_in_mem = cStringIO.StringIO(urllib.urlopen(img_url).read())
# img_bytes = Image.open(image_file_in_mem)

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': api_key,
}

params = urllib.urlencode({
    # Request parameters
    'language': 'ru',
    'detectOrientation ': 'true',
})

body = '{\'url\':\'' + img_url + '\'}'

try:
    conn = httplib.HTTPSConnection('eastus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/ocr?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
#     print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

import json
res_json = json.loads(data.decode('utf-8'))

print(json.dumps(res_json, indent=2, sort_keys=True,  ensure_ascii=False))
