BASE_URL = "https://qa-stellarburgers.education-services.ru"

# Эндпоинты
REGISTER_ENDPOINT = "/api/auth/register"
LOGIN_ENDPOINT = "/api/auth/login"
USER_ENDPOINT = "/api/auth/user"
ORDERS_ENDPOINT = "/api/orders"
INGREDIENTS_ENDPOINT = "/api/ingredients"

# Сообщения об ошибках (согласно документации API)
ERROR_USER_EXISTS = "User already exists"
ERROR_REQUIRED_FIELDS = "Email, password and name are required fields"
ERROR_INCORRECT_CREDENTIALS = "email or password are incorrect"
ERROR_NO_INGREDIENTS = "Ingredient ids must be provided"
ERROR_UNAUTHORIZED = "You should be authorised"