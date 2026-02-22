"""
Fleet Management Entity for ERP System.

This module provides entities for fleet/vehicle management
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from enum import Enum
from uuid import uuid4
from decimal import Decimal


class VehicleStatus(str, Enum):
    """Vehicle status enumeration."""
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"
    OUT_OF_SERVICE = "out_of_service"
    RESERVED = "reserved"


class VehicleType(str, Enum):
    """Vehicle type enumeration."""
    CAR = "car"
    TRUCK = "truck"
    VAN = "van"
    MOTORCYCLE = "motorcycle"
    BUS = "bus"
    HEAVY_EQUIPMENT = "heavy_equipment"


class DriverStatus(str, Enum):
    """Driver status enumeration."""
    AVAILABLE = "available"
    ON_TRIP = "on_trip"
    OFF_DUTY = "off_duty"
    SUSPENDED = "suspended"


@dataclass(frozen=True)
class VehicleLocation:
    """
    Value Object representing a vehicle location.
    Immutable and validated.
    """
    latitude: Decimal
    longitude: Decimal
    address: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "latitude": str(self.latitude),
            "longitude": str(self.longitude),
            "address": self.address,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass(frozen=True)
class FuelRecord:
    """
    Value Object representing a fuel record.
    Immutable and validated.
    """
    id: str
    date: date
    odometer_reading: int
    fuel_type: str
    quantity: Decimal
    price_per_unit: Decimal
    total_cost: Decimal
    station: str = ""
    receipt_number: str = ""
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "odometer_reading": self.odometer_reading,
            "fuel_type": self.fuel_type,
            "quantity": str(self.quantity),
            "price_per_unit": str(self.price_per_unit),
            "total_cost": str(self.total_cost),
            "station": self.station,
            "receipt_number": self.receipt_number,
            "notes": self.notes
        }


@dataclass(frozen=True)
class Vehicle:
    """
    Fleet Vehicle entity for managing vehicles.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier
        vehicle_number: Vehicle identifier/number
        make: Vehicle make
        model: Vehicle model
        year: Manufacturing year
        vin: Vehicle Identification Number
        license_plate: License plate number
        vehicle_type: Type of vehicle
        status: Current status
        current_location: Current GPS location
        odometer_reading: Current odometer reading
        fuel_level: Fuel level percentage
        fuel_capacity: Fuel tank capacity
        next_service_date: Next scheduled service
        next_service_odometer: Next service odometer reading
        insurance_expiry: Insurance expiry date
        registration_expiry: Registration expiry date
        assigned_driver_id: Assigned driver ID
        assigned_driver_name: Assigned driver name
        fuel_records: Fuel history
        total_fuel_cost: Total fuel cost
        total_mileage: Total mileage
        average_fuel_efficiency: Average MPG/L per 100km
        metadata: Additional metadata
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: str
    vehicle_number: str
    make: str
    model: str
    year: int
    vin: str
    license_plate: str
    vehicle_type: VehicleType
    status: VehicleStatus
    current_location: Optional[VehicleLocation] = None
    odometer_reading: int = 0
    fuel_level: Decimal = field(default=Decimal("100"))
    fuel_capacity: Decimal = field(default=Decimal("50"))
    next_service_date: Optional[date] = None
    next_service_odometer: Optional[int] = None
    insurance_expiry: Optional[date] = None
    registration_expiry: Optional[date] = None
    assigned_driver_id: Optional[str] = None
    assigned_driver_name: str = ""
    fuel_records: List[FuelRecord] = field(default_factory=list)
    total_fuel_cost: Decimal = field(default=Decimal("0"))
    total_mileage: int = 0
    average_fuel_efficiency: Decimal = field(default=Decimal("0"))
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.vehicle_number:
            raise ValueError("vehicle_number cannot be empty")
        if not self.vin:
            raise ValueError("vin cannot be empty")
    
    @property
    def is_available(self) -> bool:
        return self.status == VehicleStatus.AVAILABLE
    
    @property
    def is_in_maintenance(self) -> bool:
        return self.status == VehicleStatus.MAINTENANCE
    
    @property
    def needs_service(self) -> bool:
        if self.next_service_odometer and self.odometer_reading >= self.next_service_odometer:
            return True
        if self.next_service_date and date.today() >= self.next_service_date:
            return True
        return False
    
    @property
    def insurance_valid(self) -> bool:
        if not self.insurance_expiry:
            return True
        return date.today() < self.insurance_expiry
    
    @property
    def registration_valid(self) -> bool:
        if not self.registration_expiry:
            return True
        return date.today() < self.registration_expiry
    
    @property
    def is_overdue_for_service(self) -> bool:
        return self.needs_service and self.status != VehicleStatus.MAINTENANCE
    
    def update_location(self, latitude: Decimal, longitude: Decimal, address: str = "") -> None:
        """Update vehicle location."""
        self.current_location = VehicleLocation(
            latitude=latitude,
            longitude=longitude,
            address=address
        )
    
    def add_fuel_record(self, record: FuelRecord) -> None:
        """Add a fuel record and update statistics."""
        self.fuel_records.append(record)
        self.total_fuel_cost += record.total_cost
        
        if len(self.fuel_records) >= 2:
            total_fuel = sum(r.quantity for r in self.fuel_records)
            distance = self.odometer_reading - self.fuel_records[0].odometer_reading
            if total_fuel > 0 and distance > 0:
                self.average_fuel_efficiency = Decimal(str(distance / float(total_fuel)))
    
    def assign_driver(self, driver_id: str, driver_name: str) -> None:
        """Assign a driver to the vehicle."""
        self.assigned_driver_id = driver_id
        self.assigned_driver_name = driver_name
    
    def start_use(self) -> None:
        """Mark vehicle as in use."""
        self.status = VehicleStatus.IN_USE
    
    def end_use(self) -> None:
        """Mark vehicle as available."""
        self.status = VehicleStatus.AVAILABLE
    
    def send_to_maintenance(self, reason: str) -> None:
        """Send vehicle to maintenance."""
        self.status = VehicleStatus.MAINTENANCE
        self.metadata["maintenance_reason"] = reason
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "vehicle_number": self.vehicle_number,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "vin": self.vin,
            "license_plate": self.license_plate,
            "vehicle_type": self.vehicle_type.value,
            "status": self.status.value,
            "current_location": self.current_location.to_dict() if self.current_location else None,
            "odometer_reading": self.odometer_reading,
            "fuel_level": str(self.fuel_level),
            "fuel_capacity": str(self.fuel_capacity),
            "next_service_date": self.next_service_date.isoformat() if self.next_service_date else None,
            "next_service_odometer": self.next_service_odometer,
            "insurance_expiry": self.insurance_expiry.isoformat() if self.insurance_expiry else None,
            "registration_expiry": self.registration_expiry.isoformat() if self.registration_expiry else None,
            "assigned_driver_id": self.assigned_driver_id,
            "assigned_driver_name": self.assigned_driver_name,
            "fuel_records": [r.to_dict() for r in self.fuel_records],
            "total_fuel_cost": str(self.total_fuel_cost),
            "total_mileage": self.total_mileage,
            "average_fuel_efficiency": str(self.average_fuel_efficiency),
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_available": self.is_available,
            "is_in_maintenance": self.is_in_maintenance,
            "needs_service": self.needs_service,
            "insurance_valid": self.insurance_valid,
            "registration_valid": self.registration_valid,
            "is_overdue_for_service": self.is_overdue_for_service
        }


class VehicleBuilder:
    """Builder for creating Vehicle instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._vehicle_number: Optional[str] = None
        self._make: Optional[str] = None
        self._model: str = ""
        self._year: int = 0
        self._vin: Optional[str] = None
        self._license_plate: str = ""
        self._vehicle_type: VehicleType = VehicleType.CAR
        self._status: VehicleStatus = VehicleStatus.AVAILABLE
        self._odometer_reading: int = 0
        self._fuel_capacity: Decimal = Decimal("50")
        self._next_service_date: Optional[date] = None
        self._next_service_odometer: Optional[int] = None
        self._insurance_expiry: Optional[date] = None
        self._registration_expiry: Optional[date] = None
        self._assigned_driver_id: Optional[str] = None
        self._assigned_driver_name: str = ""
        self._fuel_records: List[FuelRecord] = []
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, vehicle_id: str) -> "VehicleBuilder":
        self._id = vehicle_id
        return self
    
    def with_vehicle_number(self, vehicle_number: str) -> "VehicleBuilder":
        self._vehicle_number = vehicle_number
        return self
    
    def with_details(self, make: str, model: str, year: int, vin: str) -> "VehicleBuilder":
        self._make = make
        self._model = model
        self._year = year
        self._vin = vin
        return self
    
    def with_license_plate(self, license_plate: str) -> "VehicleBuilder":
        self._license_plate = license_plate
        return self
    
    def with_vehicle_type(self, vehicle_type: VehicleType) -> "VehicleBuilder":
        self._vehicle_type = vehicle_type
        return self
    
    def with_status(self, status: VehicleStatus) -> "VehicleBuilder":
        self._status = status
        return self
    
    def with_odometer(self, reading: int) -> "VehicleBuilder":
        self._odometer_reading = reading
        return self
    
    def with_fuel_capacity(self, capacity: Decimal) -> "VehicleBuilder":
        self._fuel_capacity = capacity
        return self
    
    def with_service_schedule(self, date: date, odometer: int) -> "VehicleBuilder":
        self._next_service_date = date
        self._next_service_odometer = odometer
        return self
    
    def with_expiry_dates(self, insurance: date, registration: date) -> "VehicleBuilder":
        self._insurance_expiry = insurance
        self._registration_expiry = registration
        return self
    
    def with_driver(self, driver_id: str, driver_name: str) -> "VehicleBuilder":
        self._assigned_driver_id = driver_id
        self._assigned_driver_name = driver_name
        return self
    
    def with_fuel_records(self, records: List[FuelRecord]) -> "VehicleBuilder":
        self._fuel_records = records
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "VehicleBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Vehicle:
        if not self._id:
            self._id = str(uuid4())
        if not self._vehicle_number:
            self._vehicle_number = f"VEH-{str(self._id)[:8]}"
        if not self._vin:
            raise ValueError("vin is required")
        
        return Vehicle(
            id=self._id,
            vehicle_number=self._vehicle_number,
            make=self._make or "Unknown",
            model=self._model,
            year=self._year,
            vin=self._vin,
            license_plate=self._license_plate,
            vehicle_type=self._vehicle_type,
            status=self._status,
            odometer_reading=self._odometer_reading,
            fuel_capacity=self._fuel_capacity,
            next_service_date=self._next_service_date,
            next_service_odometer=self._next_service_odometer,
            insurance_expiry=self._insurance_expiry,
            registration_expiry=self._registration_expiry,
            assigned_driver_id=self._assigned_driver_id,
            assigned_driver_name=self._assigned_driver_name,
            fuel_records=self._fuel_records,
            metadata=self._metadata
        )


def create_vehicle(
    vin: str,
    make: str,
    model: str,
    year: int,
    **kwargs
) -> Vehicle:
    """Factory function to create a vehicle."""
    builder = VehicleBuilder()
    builder.with_details(make, model, year, vin)
    
    if vehicle_number := kwargs.get("vehicle_number"):
        builder.with_vehicle_number(vehicle_number)
    if license_plate := kwargs.get("license_plate"):
        builder.with_license_plate(license_plate)
    if vehicle_type := kwargs.get("vehicle_type"):
        builder.with_vehicle_type(vehicle_type)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if odometer_reading := kwargs.get("odometer_reading"):
        builder.with_odometer(odometer_reading)
    if fuel_capacity := kwargs.get("fuel_capacity"):
        builder.with_fuel_capacity(fuel_capacity)
    if next_service_date := kwargs.get("next_service_date"):
        next_service_odometer = kwargs.get("next_service_odometer", 10000)
        builder.with_service_schedule(next_service_date, next_service_odometer)
    if insurance_expiry := kwargs.get("insurance_expiry"):
        registration_expiry = kwargs.get("registration_expiry")
        builder.with_expiry_dates(insurance_expiry, registration_expiry)
    if assigned_driver_id := kwargs.get("assigned_driver_id"):
        assigned_driver_name = kwargs.get("assigned_driver_name", "")
        builder.with_driver(assigned_driver_id, assigned_driver_name)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()


def create_fuel_record(
    date: date,
    odometer_reading: int,
    fuel_type: str,
    quantity: Decimal,
    price_per_unit: Decimal,
    **kwargs
) -> FuelRecord:
    """Factory function to create a fuel record."""
    return FuelRecord(
        id=str(uuid4()),
        date=date,
        odometer_reading=odometer_reading,
        fuel_type=fuel_type,
        quantity=quantity,
        price_per_unit=price_per_unit,
        total_cost=quantity * price_per_unit,
        station=kwargs.get("station", ""),
        receipt_number=kwargs.get("receipt_number", ""),
        notes=kwargs.get("notes", "")
    )
