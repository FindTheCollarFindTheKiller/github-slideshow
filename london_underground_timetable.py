"""
London Underground Timetable System

This module provides a comprehensive coding solution for managing and querying
the London Underground rail network timetable.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class LineColor(Enum):
    """London Underground line colors"""
    BAKERLOO = "Bakerloo"
    CENTRAL = "Central"
    CIRCLE = "Circle"
    DISTRICT = "District"
    HAMMERSMITH_CITY = "Hammersmith & City"
    JUBILEE = "Jubilee"
    METROPOLITAN = "Metropolitan"
    NORTHERN = "Northern"
    PICCADILLY = "Piccadilly"
    VICTORIA = "Victoria"
    WATERLOO_CITY = "Waterloo & City"


@dataclass
class Station:
    """Represents a London Underground station"""
    name: str
    code: str
    zone: int
    interchange: bool = False
    lines: List[str] = field(default_factory=list)
    
    def __str__(self) -> str:
        return f"{self.name} (Zone {self.zone})"
    
    def __repr__(self) -> str:
        return f"Station(name='{self.name}', code='{self.code}', zone={self.zone})"


@dataclass
class Service:
    """Represents a train service on a specific line"""
    service_id: str
    line: str
    direction: str
    stations: List[str]
    
    def __str__(self) -> str:
        return f"{self.line} Line - {self.direction} ({len(self.stations)} stations)"


@dataclass
class ScheduledStop:
    """Represents a scheduled stop at a station"""
    station_code: str
    arrival_time: datetime
    departure_time: datetime
    platform: Optional[str] = None
    
    def __str__(self) -> str:
        return f"{self.station_code}: Arr {self.arrival_time.strftime('%H:%M')} / Dep {self.departure_time.strftime('%H:%M')}"


@dataclass
class Train:
    """Represents a train with its schedule"""
    train_id: str
    service: Service
    stops: List[ScheduledStop]
    operating: bool = True
    
    def get_departure_time(self, station_code: str) -> Optional[datetime]:
        """Get departure time from a specific station"""
        for stop in self.stops:
            if stop.station_code == station_code:
                return stop.departure_time
        return None
    
    def get_arrival_time(self, station_code: str) -> Optional[datetime]:
        """Get arrival time at a specific station"""
        for stop in self.stops:
            if stop.station_code == station_code:
                return stop.arrival_time
        return None


class LondonUndergroundTimetable:
    """Main timetable system for London Underground"""
    
    def __init__(self):
        self.stations: Dict[str, Station] = {}
        self.services: Dict[str, Service] = {}
        self.trains: List[Train] = []
        self._initialize_network()
    
    def _initialize_network(self):
        """Initialize the London Underground network with stations and lines"""
        # Add major stations on Central Line
        self._add_station("Liverpool Street", "LVS", 1, True, ["Central", "Circle", "Hammersmith & City", "Metropolitan"])
        self._add_station("Bank", "BNK", 1, True, ["Central", "Northern", "Waterloo & City"])
        self._add_station("Oxford Circus", "OXC", 1, True, ["Central", "Victoria", "Bakerloo"])
        self._add_station("Tottenham Court Road", "TCR", 1, True, ["Central", "Northern"])
        self._add_station("Bond Street", "BST", 1, True, ["Central", "Jubilee"])
        self._add_station("Marble Arch", "MAR", 1, False, ["Central"])
        self._add_station("Lancaster Gate", "LGT", 1, False, ["Central"])
        self._add_station("Queensway", "QWY", 1, False, ["Central"])
        self._add_station("Notting Hill Gate", "NHG", 1, True, ["Central", "Circle", "District"])
        
        # Add major stations on Northern Line
        self._add_station("King's Cross St Pancras", "KGX", 1, True, ["Northern", "Piccadilly", "Victoria", "Circle", "Hammersmith & City", "Metropolitan"])
        self._add_station("Euston", "EUS", 1, True, ["Northern", "Victoria"])
        self._add_station("Camden Town", "CMD", 2, False, ["Northern"])
        self._add_station("Hampstead", "HAM", 3, False, ["Northern"])
        self._add_station("Waterloo", "WAT", 1, True, ["Northern", "Bakerloo", "Jubilee", "Waterloo & City"])
        
        # Add major stations on Piccadilly Line
        self._add_station("Leicester Square", "LSQ", 1, True, ["Northern", "Piccadilly"])
        self._add_station("Piccadilly Circus", "PIC", 1, True, ["Piccadilly", "Bakerloo"])
        self._add_station("Green Park", "GPK", 1, True, ["Piccadilly", "Victoria", "Jubilee"])
        self._add_station("Hyde Park Corner", "HPC", 1, False, ["Piccadilly"])
        self._add_station("Knightsbridge", "KNB", 1, False, ["Piccadilly"])
        
        # Add major stations on Victoria Line
        self._add_station("Victoria", "VIC", 1, True, ["Victoria", "Circle", "District"])
        self._add_station("Warren Street", "WST", 1, True, ["Victoria", "Northern"])
        
        # Initialize sample services
        self._initialize_services()
        self._generate_sample_timetable()
    
    def _add_station(self, name: str, code: str, zone: int, interchange: bool, lines: List[str]):
        """Add a station to the network"""
        station = Station(name=name, code=code, zone=zone, interchange=interchange, lines=lines)
        self.stations[code] = station
    
    def _initialize_services(self):
        """Initialize line services"""
        # Central Line - Eastbound
        central_eb = Service(
            service_id="CEN_EB",
            line="Central",
            direction="Eastbound",
            stations=["NHG", "QWY", "LGT", "MAR", "BST", "OXC", "TCR", "BNK", "LVS"]
        )
        self.services["CEN_EB"] = central_eb
        
        # Central Line - Westbound
        central_wb = Service(
            service_id="CEN_WB",
            line="Central",
            direction="Westbound",
            stations=["LVS", "BNK", "TCR", "OXC", "BST", "MAR", "LGT", "QWY", "NHG"]
        )
        self.services["CEN_WB"] = central_wb
        
        # Northern Line - Northbound
        northern_nb = Service(
            service_id="NTH_NB",
            line="Northern",
            direction="Northbound",
            stations=["WAT", "BNK", "LSQ", "TCR", "KGX", "EUS", "CMD", "HAM"]
        )
        self.services["NTH_NB"] = northern_nb
        
        # Northern Line - Southbound
        northern_sb = Service(
            service_id="NTH_SB",
            line="Northern",
            direction="Southbound",
            stations=["HAM", "CMD", "EUS", "KGX", "TCR", "LSQ", "BNK", "WAT"]
        )
        self.services["NTH_SB"] = northern_sb
    
    def _generate_sample_timetable(self):
        """Generate sample train schedules"""
        base_time = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
        
        # Generate Central Line trains (every 3-5 minutes during peak)
        for i in range(20):
            # Eastbound
            departure_time = base_time + timedelta(minutes=i * 4)
            self._create_train(f"CE{i:03d}", "CEN_EB", departure_time, 2)
            
            # Westbound
            departure_time = base_time + timedelta(minutes=i * 4 + 2)
            self._create_train(f"CW{i:03d}", "CEN_WB", departure_time, 2)
        
        # Generate Northern Line trains (every 3-4 minutes during peak)
        for i in range(25):
            # Northbound
            departure_time = base_time + timedelta(minutes=i * 3.5)
            self._create_train(f"NN{i:03d}", "NTH_NB", departure_time, 2.5)
            
            # Southbound
            departure_time = base_time + timedelta(minutes=i * 3.5 + 1)
            self._create_train(f"NS{i:03d}", "NTH_SB", departure_time, 2.5)
    
    def _create_train(self, train_id: str, service_id: str, start_time: datetime, minutes_per_stop: float):
        """Create a train with scheduled stops"""
        service = self.services[service_id]
        stops = []
        current_time = start_time
        
        for station_code in service.stations:
            arrival_time = current_time
            departure_time = current_time + timedelta(minutes=1)  # 1 minute dwell time
            
            stop = ScheduledStop(
                station_code=station_code,
                arrival_time=arrival_time,
                departure_time=departure_time
            )
            stops.append(stop)
            
            current_time = departure_time + timedelta(minutes=minutes_per_stop)
        
        train = Train(train_id=train_id, service=service, stops=stops)
        self.trains.append(train)
    
    def get_station(self, code: str) -> Optional[Station]:
        """Get station by code"""
        return self.stations.get(code)
    
    def find_station_by_name(self, name: str) -> Optional[Station]:
        """Find station by name"""
        for station in self.stations.values():
            if station.name.lower() == name.lower():
                return station
        return None
    
    def get_next_trains(self, station_code: str, line: Optional[str] = None, 
                       count: int = 5, after_time: Optional[datetime] = None) -> List[Tuple[Train, datetime]]:
        """Get next trains departing from a station"""
        if after_time is None:
            after_time = datetime.now()
        
        departures = []
        for train in self.trains:
            if not train.operating:
                continue
            
            # Filter by line if specified
            if line and train.service.line != line:
                continue
            
            departure_time = train.get_departure_time(station_code)
            if departure_time and departure_time > after_time:
                departures.append((train, departure_time))
        
        # Sort by departure time and return top N
        departures.sort(key=lambda x: x[1])
        return departures[:count]
    
    def get_journey_time(self, from_station: str, to_station: str, 
                        train_id: str) -> Optional[timedelta]:
        """Calculate journey time between two stations on a specific train"""
        train = next((t for t in self.trains if t.train_id == train_id), None)
        if not train:
            return None
        
        departure = train.get_departure_time(from_station)
        arrival = train.get_arrival_time(to_station)
        
        if departure and arrival:
            return arrival - departure
        return None
    
    def get_all_trains_on_line(self, line: str) -> List[Train]:
        """Get all trains operating on a specific line"""
        return [train for train in self.trains if train.service.line == line]
    
    def get_interchanges(self) -> List[Station]:
        """Get all interchange stations"""
        return [station for station in self.stations.values() if station.interchange]
    
    def print_station_info(self, station_code: str):
        """Print detailed information about a station"""
        station = self.get_station(station_code)
        if not station:
            print(f"Station {station_code} not found")
            return
        
        print(f"\n{'='*60}")
        print(f"Station: {station.name}")
        print(f"Code: {station.code}")
        print(f"Zone: {station.zone}")
        print(f"Interchange: {'Yes' if station.interchange else 'No'}")
        print(f"Lines: {', '.join(station.lines)}")
        print(f"{'='*60}\n")
    
    def print_next_departures(self, station_code: str, line: Optional[str] = None):
        """Print next departures from a station"""
        station = self.get_station(station_code)
        if not station:
            print(f"Station {station_code} not found")
            return
        
        print(f"\n{'='*60}")
        print(f"Next departures from {station.name}")
        if line:
            print(f"Line: {line}")
        print(f"{'='*60}")
        
        departures = self.get_next_trains(station_code, line, count=10)
        
        if not departures:
            print("No departures found")
            return
        
        for train, departure_time in departures:
            print(f"{departure_time.strftime('%H:%M')} - {train.service.line} Line "
                  f"({train.service.direction}) - Train {train.train_id}")
        print(f"{'='*60}\n")


def main():
    """Example usage of the London Underground Timetable system"""
    print("London Underground Timetable System")
    print("=" * 60)
    
    # Initialize the timetable
    timetable = LondonUndergroundTimetable()
    
    # Print system statistics
    print(f"\nNetwork Statistics:")
    print(f"  Total Stations: {len(timetable.stations)}")
    print(f"  Interchange Stations: {len(timetable.get_interchanges())}")
    print(f"  Total Services: {len(timetable.services)}")
    print(f"  Total Trains: {len(timetable.trains)}")
    
    # Example 1: Show station information
    print("\n" + "="*60)
    print("Example 1: Station Information")
    timetable.print_station_info("OXC")
    
    # Example 2: Show next departures from Oxford Circus
    print("\n" + "="*60)
    print("Example 2: Next Departures")
    timetable.print_next_departures("OXC")
    
    # Example 3: Show next Central Line trains from Bond Street
    print("\n" + "="*60)
    print("Example 3: Next Central Line Trains")
    timetable.print_next_departures("BST", line="Central")
    
    # Example 4: List all interchange stations
    print("\n" + "="*60)
    print("Example 4: Interchange Stations")
    print("="*60)
    interchanges = timetable.get_interchanges()
    for station in interchanges:
        print(f"  {station.name} (Zone {station.zone}): {', '.join(station.lines)}")
    
    # Example 5: Calculate journey time
    print("\n" + "="*60)
    print("Example 5: Journey Time Calculation")
    print("="*60)
    train = timetable.trains[0]
    if len(train.stops) >= 2:
        from_station = train.stops[0].station_code
        to_station = train.stops[-1].station_code
        journey_time = timetable.get_journey_time(from_station, to_station, train.train_id)
        if journey_time:
            from_name = timetable.get_station(from_station).name
            to_name = timetable.get_station(to_station).name
            print(f"  Train {train.train_id}")
            print(f"  From: {from_name}")
            print(f"  To: {to_name}")
            print(f"  Journey Time: {int(journey_time.total_seconds() / 60)} minutes")
    
    print("\n" + "="*60)
    print("Timetable system demonstration complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
