class DependencyInjector:
    _registered_classes = {}

    @classmethod
    def register_class(cls, key, class_instance):
        cls._registered_classes[key] = class_instance

    @classmethod
    def get_instance(cls, key):
        if key not in cls._registered_classes:
            raise ValueError(f"Class with key '{key}' not registered.")
        return cls._registered_classes[key]()


