from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, make: str, model: str):
        self.make = make
        self.model = model

    @abstractmethod
    def start_engine(self) -> None:
        pass

class Car(Vehicle):
    def start_engine(self):
        print(f"{self.make} {self.model}: Двигун запущено")

class Motorcycle(Vehicle):
    def start_engine(self):
        print(f"{self.make} {self.model}: Мотор заведено")

class VehicleFactory:
    SPEC_LABEL = ""

    @classmethod
    def create_car(self, make, model):
        return Car(make, f"{model} ({self.SPEC_LABEL})")

    @classmethod
    def create_motorcycle(self, make, model):
        return Motorcycle(make, f"{model} ({self.SPEC_LABEL})")

class USVehicleFactory(VehicleFactory):
    SPEC_LABEL = "US Spec"

class EUVehicleFactory(VehicleFactory):
    SPEC_LABEL = "EU Spec"

if __name__ == "__main__":
    vehicle1 = USVehicleFactory.create_car("Ford", "Mustang")
    vehicle1.start_engine()  # Ford Mustang (US Spec): Двигун запущено

    vehicle2 = EUVehicleFactory.create_motorcycle("Harley-Davidson", "Sportster")
    vehicle2.start_engine()  # Harley-Davidson Sportster (EU Spec): Мотор заведено