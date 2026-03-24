import os
import pytest
import json
from config import *
from models import *

@pytest.fixture(scope="module")
def test_get_client_by_id(client, sample_data):
  """Test retrieving a specific client."""
  client_id = sample_data['client'].id
  
  response = client.get(f'/clients/{client_id}')
  
  assert response.status_code == 200
  data = json.loads(response.data)
  assert data['name'] == 'Acme Corp'
  assert data['contact'] == 'john@acme.com'
  assert data['active'] == True

def test_create_client(client, sample_data):
  """Test creating a new client."""
  new_client = {
      'name': 'TechStart Inc',
      'contact': 'contact@techstart.com',
      'active': True
  }
  
  response = client.post(
      '/clients',
      data=json.dumps(new_client),
      content_type='application/json'
  )
  
  assert response.status_code == 201
  data = json.loads(response.data)
  assert data['name'] == 'TechStart Inc'
  assert data['contact'] == 'contact@techstart.com'