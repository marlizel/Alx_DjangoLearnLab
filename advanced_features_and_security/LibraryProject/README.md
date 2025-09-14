# LibraryProject

This project is a Django application that manages a library system. It demonstrates the use of a custom user model and implements a robust permissions system using Django's built-in features.

### Permissions and Groups

Permissions for the `Book` model are defined in `bookshelf/models.py`.

Permissions are enforced in `bookshelf/views.py` using the `@permission_required` decorator to restrict access to the `book_list` view.

Groups such as 'Admins', 'Editors', and 'Viewers' are configured in the Django admin panel, with specific permissions assigned to each group. This allows for fine-grained access control based on user roles.