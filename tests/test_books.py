from app.books.schemas import BookCreateSchema
from app.books.models import Book
from datetime import datetime


def test_add_book(client, mocker):
    # Mock the UserService to return a user
    mocker.patch('app.users.services.UserService.get_user_by_id', return_value={'id': 1, 'username': 'testuser'})

    # Define the book data
    book_data = BookCreateSchema(
        title='Test Book',
        user_id=1
    ).model_dump()

    # Send a POST request to add a book
    response = client.post('api/books/', json=book_data)

    # Assert the response status code and content
    assert response.status_code == 201
    assert response.json['status'] == 'book added successfully'
    assert response.json['book']['title'] == 'Test Book'
    assert response.json['book']['user_id'] == 1


def test_list_books(client, mocker):
    # Mock the UserService to return a user
    mocker.patch('app.users.services.UserService.get_user_by_id', return_value={'id': 1, 'username': 'testuser'})

    # Define the book data
    book_data1 = BookCreateSchema(
        title='Test Book',
        user_id=1
    ).model_dump()
    # Another book for the same user
    book_data2 = BookCreateSchema(
        title='Another Test Book',
        user_id=1
    ).model_dump()
    # Send a POST request to add two books
    client.post('api/books/', json=book_data1)
    client.post('api/books/', json=book_data2)

    # Send a GET request to list books for user with ID 1
    response = client.get('api/books/1')

    # Assert the response status code and content
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]['title'] == 'Test Book'


def test_get_recommendations(client, mocker):
    # Mock the UserService to return a user
    mocker.patch('app.users.services.UserService.get_user_by_id', return_value={'id': 1, 'username': 'testuser'})

    # Mock BookService con objetos reales
    mocker.patch('app.books.services.BookService.get_books_by_user_id', return_value=[
        Book(id=1, title='Test Book 1', timestamp=datetime(2023, 10, 1), user_id=1),
        Book(id=2, title='Test Book 2', timestamp=datetime(2023, 10, 2), user_id=1)
    ])
    # Send a GET request to get recommendations for user with ID 1
    response = client.get('api/books/recommendations/1')

    # Assert the response status code and content
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0
    assert 'explanation' in response.json[0]
