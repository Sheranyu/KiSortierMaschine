from injector import inject, Module, Binder, Injector

# Service-Klassen
class UserRepository:
    def get_user(self, user_id):
        return f"User {user_id}"

class UserService:
    @inject
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user_info(self, user_id):
        return self.user_repository.get_user(user_id)

# Ein einfaches Modul für die Konfiguration der Dependency Injection
class MyModule(Module):
    def configure(self, binder: Binder):
        binder.bind(UserRepository)

# Hauptklasse, die die Abhängigkeiten verwendet
@inject
class SomeController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def print_user_info(self, user_id):
        user_info = self.user_service.get_user_info(user_id)
        print(f"User Info: {user_info}")

# Konfiguration und Erstellung der Dependency Injection
if __name__ == "__main__":
    injector = Injector([MyModule()])
    controller = injector.get(SomeController)

    # Verwendung der erstellten Instanz von SomeController
    controller.print_user_info(123)
