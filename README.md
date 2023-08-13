# Theatre Management API

The Theatre Management API is a Django-based web application designed to facilitate the management of plays, performances, reservations, and related data for a theatre. This API provides various endpoints for administrators and authenticated users to interact with the system. It includes features such as viewing and filtering plays, managing performances, creating reservations, and more.

## Getting Started

### Prerequisites

Before you begin, make sure you have the following tools and technologies installed:

- Python (>=3.6)
- Django
- Django REST framework

## Installing / Getting started

A quick introduction of the setup you need to get run a project.
1. Fork a repo.
2. Use this command ```git clone the-link-from-your-forked-repo```. 
   - You can get the link by clicking the Clone or download button in your repo.
3. Open the project folder in your IDE.
4. Open a terminal in the project folder. 
5. If you are using PyCharm - it may propose you to automatically create venv for your project and install requirements in it, but if not:
    - For Windows:
    ```shell
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```
   - For Mac OS:
    ```shell
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
   ```
6. Run create migration file, using 
    ```shell
    python manage.py makemigrations
    ```
    Then migrate file, using
    ```shell
    python manage.py migrate
    ```
7. Load data to the db using this command:
   ```shell
   python manage.py loaddata theatre_service_db_data.json
   ```
8. You can use this admin user:
   - Email: `admin.user@cinema.com`
   - Password: `1qazcde3`

   Or you can create superuser by yourself:
      ```shell
      python manage.py createsuperuser
      ```
9. Start the development server:
   ```shell
   python manage.py runserver
   ```
## API Endpoints

<details>
  <summary>Actors</summary>
  
- **List Actors**: `GET /api/theatre/actors/`
- **Create Actor**: `POST /api/theatre/actors/`
- **Retrieve Actor**: `GET /api/theatre/actors/{actor_id}/`
- **Update Actor**: `PUT /api/theatre/actors/{actor_id}/`
- **Partial Update** `PATCH /api/theatre/actors/{actor_id}/`
- **Delete Actor**: `DELETE /api/theatre/actors/{actor_id}/`
</details>

<details>
  <summary>Genres</summary>
  
- **List Genres**: `GET /api/theatre/genres/`
- **Create Genre**: `POST /api/theatre/genres/`
- **Retrieve Genre**: `GET /api/theatre/genres/{genre_id}/`
- **Update Genre**: `PUT /api/theatre/genres/{genre_id}/`
- **Partial Update**: `PATCH /api/theatre/genres/{genre_id}/`
- **Delete Genre**: `DELETE /api/theatre/genres/{genre_id}/`
</details>

<details>
  <summary>Performances</summary>
  
- **List Performances**: `GET /api/theatre/performances/`
- **Create Performance**: `POST /api/theatre/performances/`
- **Retrieve Performance**: `GET /api/theatre/performances/{performance_id}/`
- **Update Performance**: `PUT /api/theatre/performances/{performance_id}/`
- **Partial Update** `PATCH /api/theatre/performances/{performance_id}/`
- **Delete Performance**: `DELETE /api/theatre/performances/{performance_id}/`
</details>

<details>
  <summary>Plays</summary>
  
- **List Plays**: `GET /api/theatre/plays/`
- **Create Play**: `POST /api/theatre/plays/`
- **Retrieve Play**: `GET /api/theatre/plays/{play_id}/`
- **Update Play**: `PUT /api/theatre/plays/{play_id}/`
- **Partial Update** `PATCH /api/theatre/plays/{play_id}/`
- **Delete Play**: `DELETE /api/theatre/plays/{play_id}/`
- **Image Upload**: `POST /api/theatre/plays/{play_id}/upload-image/`
</details>

<details>
  <summary>Reservations</summary>
  
- **List Reservations**: `GET /api/theatre/reservations/`
- **Create Reservation**: `POST /api/theatre/reservations/`
- **Retrieve Reservation**: `GET /api/theatre/reservations/{reservation_id}/`
- **Update Reservation**: `PUT /api/theatre/reservations/{reservation_id}/`
- **Partial Update** `PATCH /api/theatre/reservations/{reservation_id}/`
- **Delete Reservation**: `DELETE /api/theatre/reservations/{reservation_id}/`
</details>

<details>
  <summary>Theatre Halls</summary>
  
- **List Theatre Halls**: `GET /api/theatre/theatre_halls/`
- **Create Theatre Hall**: `POST /api/theatre/theatre_halls/`
- **Retrieve Theatre Hall**: `GET /api/theatre/theatre_halls/{theatre_hall_id}/`
- **Update Theatre Hall**: `PUT /api/theatre/theatre_halls/{theatre_hall_id}/`
- **Partial Update** `PATCH /api/theatre/theatre_halls/{theatre_hall_id}/`
- **Delete Theatre Hall**: `DELETE /api/theatre/theatre_halls/{theatre_hall_id}/`
</details>

<details>
  <summary>User</summary>
  
- **Information about current User**: `GET /api/user/me/`
- **Update User**: `PUT /api/user/me/`
- **Partial Update** `PATCH /api/user/me/`
- **Create new User** `POST /api/user/register/`
- **Create access and refresh tokens** `POST /api/user/token/`
- **Refresh access token** `POST /api/user/token/refresh/`
- **Verify tokens**: `POST /api/user/token/verify/`
</details>


## Authentication
- The API uses token-based authentication for user access. Users need to obtain an authentication token by logging in.
- Administrators and authenticated users can access all endpoints, but only administrator can change information about plays, performances, genres, etc. However, each authenticated user can access and create their own reservations.

## Documentation
- The API is documented using the OpenAPI standard.
- Access the API documentation by running the server and navigating to http://localhost:8000/api/doc/swagger/ or http://localhost:8000/api/doc/redoc/.

## License
This project is licensed under the MIT License.