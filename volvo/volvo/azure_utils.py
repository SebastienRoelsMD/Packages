import os    
from azure.storage.blob import BlockBlobService
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential


CLIENT_ID = '4b53bd8b-c698-479c-a9bb-464bcaf10ba0'
CLIENT_SECRET = 'QT65-xIYJv4_kLxDRN8B5Ow4E1k0-64~mG'
TENANT_ID = 'f25493ae-1c98-41d7-8a33-0be75f5fe603'
VAULT_NAME = 'smleurope-dev-weu-rg'
VAULT_URI = 'https://smleurope-dev-weu-kv.vault.azure.net/'

credential = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
client = SecretClient(vault_url=VAULT_URI, credential=credential)

#client.get_secret('github-da')


STORAGE_ACCOUNT = 'smleuropedevweusa'
STORAGE_KEY = 'x3dMwsiGRfceIPoFjej78WbWculgS01LJm+NSbfpu6WLUNdeld7dBPb3O5xQhaeTy3EF+0xJ3jHAFLpoyH2T/Q=='
CONTAINER = 'excel-files'

os.environ['http_proxy']="http://httppxgot.srv.volvo.com:8080"
os.environ['https_proxy']="https://httppxgot.srv.volvo.com:8080"
    
blob_service = BlockBlobService(STORAGE_ACCOUNT, STORAGE_KEY)


def get_file(filename):
    
    blob_service.get_blob_to_path(CONTAINER, filename, filename)
    
def remove_file(filename):
    
    """
    Remove LOCAL file
    """
    
    os.remove(filename)
    
def create_file(filename, path):
    
    """
    path should include filename
    """
    
    blob_service.create_blob_from_path(CONTAINER, filename, path)
    