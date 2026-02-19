import pytest
import json
from main import app, items, item_id_counter


@pytest.fixture(autouse=True)
def reset_state():
    """Reset global state before each test"""
    items.clear()
    global item_id_counter
    item_id_counter = 1
    yield


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHomeEndpoint:
    """Test cases for the home endpoint"""
    
    def test_home(self, client):
        """Test the home endpoint returns welcome message"""
        rv = client.get('/')
        assert rv.status_code == 200
        data = json.loads(rv.data)
        assert 'message' in data
        assert data['message'] == "Welcome to the Flask API"
        assert 'endpoints' in data


class TestCreateItem:
    """Test cases for creating items"""
    
    def test_create_item_success(self, client):
        """Test creating a new item successfully"""
        rv = client.post('/items',
                        data=json.dumps({'name': 'Test Item', 'description': 'A test item'}),
                        content_type='application/json')
        assert rv.status_code == 201
        data = json.loads(rv.data)
        assert data['id'] == 1
        assert data['name'] == 'Test Item'
        assert data['description'] == 'A test item'
    
    def test_create_item_without_description(self, client):
        """Test creating an item without description"""
        rv = client.post('/items',
                        data=json.dumps({'name': 'Simple Item'}),
                        content_type='application/json')
        assert rv.status_code == 201
        data = json.loads(rv.data)
        assert data['name'] == 'Simple Item'
        assert data['description'] == ''
    
    def test_create_item_missing_name(self, client):
        """Test creating an item without name returns 400"""
        rv = client.post('/items',
                        data=json.dumps({'description': 'No name'}),
                        content_type='application/json')
        assert rv.status_code == 400
        data = json.loads(rv.data)
        assert 'error' in data
    
    def test_create_item_empty_body(self, client):
        """Test creating an item with empty body returns 400"""
        rv = client.post('/items',
                        data=json.dumps({}),
                        content_type='application/json')
        assert rv.status_code == 400


class TestGetItems:
    """Test cases for getting items"""
    
    def test_get_items_empty(self, client):
        """Test getting items when none exist"""
        rv = client.get('/items')
        assert rv.status_code == 200
        data = json.loads(rv.data)
        assert data['items'] == []
    
    def test_get_items_with_data(self, client):
        """Test getting items after creating some"""
        # Create two items
        client.post('/items',
                   data=json.dumps({'name': 'Item 1'}),
                   content_type='application/json')
        client.post('/items',
                   data=json.dumps({'name': 'Item 2'}),
                   content_type='application/json')
        
        rv = client.get('/items')
        assert rv.status_code == 200
        data = json.loads(rv.data)
        assert len(data['items']) == 2
        assert data['items'][0]['name'] == 'Item 1'
        assert data['items'][1]['name'] == 'Item 2'


class TestGetItemById:
    """Test cases for getting a specific item"""
    
    def test_get_item_success(self, client):
        """Test getting an existing item by ID"""
        # Create an item first
        rv = client.post('/items',
                        data=json.dumps({'name': 'Specific Item'}),
                        content_type='application/json')
        item_id = json.loads(rv.data)['id']
        
        # Get the item
        rv = client.get(f'/items/{item_id}')
        assert rv.status_code == 200
        data = json.loads(rv.data)
        assert data['id'] == item_id
        assert data['name'] == 'Specific Item'
    
    def test_get_item_not_found(self, client):
        """Test getting a non-existent item returns 404"""
        rv = client.get('/items/999')
        assert rv.status_code == 404
        data = json.loads(rv.data)
        assert 'error' in data


class TestUpdateItem:
    """Test cases for updating items"""
    
    def test_update_item_name(self, client):
        """Test updating an item's name"""
        # Create an item
        rv = client.post('/items',
                        data=json.dumps({'name': 'Original Name'}),
                        content_type='application/json')
        item_id = json.loads(rv.data)['id']
        
        # Update the item
        rv = client.put(f'/items/{item_id}',
                       data=json.dumps({'name': 'Updated Name'}),
                       content_type='application/json')
        assert rv.status_code == 200
        data = json.loads(rv.data)
        assert data['name'] == 'Updated Name'
        assert data['id'] == item_id
    
    def test_update_item_description(self, client):
        """Test updating an item's description"""
        # Create an item
        rv = client.post('/items',
                        data=json.dumps({'name': 'Test', 'description': 'Original'}),
                        content_type='application/json')
        item_id = json.loads(rv.data)['id']
        
        # Update the item
        rv = client.put(f'/items/{item_id}',
                       data=json.dumps({'description': 'Updated description'}),
                       content_type='application/json')
        assert rv.status_code == 200
        data = json.loads(rv.data)
        assert data['description'] == 'Updated description'
    
    def test_update_item_both_fields(self, client):
        """Test updating both name and description"""
        # Create an item
        rv = client.post('/items',
                        data=json.dumps({'name': 'Old', 'description': 'Old desc'}),
                        content_type='application/json')
        item_id = json.loads(rv.data)['id']
        
        # Update the item
        rv = client.put(f'/items/{item_id}',
                       data=json.dumps({'name': 'New', 'description': 'New desc'}),
                       content_type='application/json')
        assert rv.status_code == 200
        data = json.loads(rv.data)
        assert data['name'] == 'New'
        assert data['description'] == 'New desc'
    
    def test_update_item_not_found(self, client):
        """Test updating a non-existent item returns 404"""
        rv = client.put('/items/999',
                       data=json.dumps({'name': 'Test'}),
                       content_type='application/json')
        assert rv.status_code == 404


class TestDeleteItem:
    """Test cases for deleting items"""
    
    def test_delete_item_success(self, client):
        """Test deleting an existing item"""
        # Create an item
        rv = client.post('/items',
                        data=json.dumps({'name': 'To Delete'}),
                        content_type='application/json')
        item_id = json.loads(rv.data)['id']
        
        # Delete the item
        rv = client.delete(f'/items/{item_id}')
        assert rv.status_code == 200
        data = json.loads(rv.data)
        assert 'message' in data
        
        # Verify item is deleted
        rv = client.get(f'/items/{item_id}')
        assert rv.status_code == 404
    
    def test_delete_item_not_found(self, client):
        """Test deleting a non-existent item returns 404"""
        rv = client.delete('/items/999')
        assert rv.status_code == 404