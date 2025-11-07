# London Underground Timetable System

A comprehensive Python implementation for managing and querying the London Underground rail network timetable.

## Overview

This system provides a complete coding solution for modeling the London Underground network, including:

- **Station Management**: Store and retrieve information about stations, zones, and interchange points
- **Line Services**: Define routes and directions for different Underground lines
- **Train Scheduling**: Generate and manage train timetables with arrival/departure times
- **Query Interface**: Find next trains, calculate journey times, and get station information

## Features

### Core Components

1. **Station Class**
   - Station name, code, and zone information
   - Interchange status
   - Associated lines

2. **Service Class**
   - Line identification
   - Direction (Eastbound/Westbound/Northbound/Southbound)
   - Station sequence

3. **Train Class**
   - Unique train ID
   - Service assignment
   - Scheduled stops with arrival/departure times
   - Operating status

4. **Timetable System**
   - Network initialization
   - Train generation
   - Query and search capabilities

### Supported Lines

The current implementation includes major stations on:
- Central Line
- Northern Line
- Piccadilly Line
- Victoria Line

Additional lines can be easily added following the same pattern.

## Installation

No external dependencies required! The system uses only Python standard library.

```bash
# Python 3.7+ required
python3 london_underground_timetable.py
```

## Usage

### Basic Example

```python
from london_underground_timetable import LondonUndergroundTimetable

# Initialize the timetable system
timetable = LondonUndergroundTimetable()

# Get station information
station = timetable.get_station("OXC")  # Oxford Circus
print(f"Station: {station.name}, Zone: {station.zone}")

# Find next trains from a station
departures = timetable.get_next_trains("OXC", count=5)
for train, departure_time in departures:
    print(f"{departure_time.strftime('%H:%M')} - {train.service.line} Line")

# Get all trains on a specific line
central_trains = timetable.get_all_trains_on_line("Central")
print(f"Trains on Central Line: {len(central_trains)}")

# Calculate journey time
journey_time = timetable.get_journey_time("OXC", "LVS", "CE001")
if journey_time:
    print(f"Journey time: {int(journey_time.total_seconds() / 60)} minutes")
```

### Advanced Queries

```python
# Get next trains on a specific line only
next_central = timetable.get_next_trains("BST", line="Central", count=10)

# Find all interchange stations
interchanges = timetable.get_interchanges()
for station in interchanges:
    print(f"{station.name}: {', '.join(station.lines)}")

# Search station by name
station = timetable.find_station_by_name("Bank")
if station:
    print(f"Station code: {station.code}")
```

### Display Methods

```python
# Print formatted station information
timetable.print_station_info("OXC")

# Print next departures board
timetable.print_next_departures("OXC")
timetable.print_next_departures("BST", line="Central")
```

## Data Structure

### Station Codes

| Code | Station Name | Zone | Lines |
|------|-------------|------|-------|
| OXC | Oxford Circus | 1 | Central, Victoria, Bakerloo |
| BST | Bond Street | 1 | Central, Jubilee |
| BNK | Bank | 1 | Central, Northern, Waterloo & City |
| KGX | King's Cross St Pancras | 1 | Northern, Piccadilly, Victoria, Circle, H&C, Metropolitan |
| WAT | Waterloo | 1 | Northern, Bakerloo, Jubilee, Waterloo & City |

### Service IDs

- **CEN_EB**: Central Line Eastbound
- **CEN_WB**: Central Line Westbound
- **NTH_NB**: Northern Line Northbound
- **NTH_SB**: Northern Line Southbound

## Architecture

### Class Hierarchy

```
LondonUndergroundTimetable
├── stations: Dict[str, Station]
├── services: Dict[str, Service]
└── trains: List[Train]
    └── stops: List[ScheduledStop]
```

### Data Flow

1. **Initialization**: Network is populated with stations and line services
2. **Generation**: Trains are generated with scheduled stops based on services
3. **Query**: Users can query trains, stations, and calculate journey times

## Extending the System

### Adding New Stations

```python
def _add_station(self, name: str, code: str, zone: int, 
                 interchange: bool, lines: List[str]):
    station = Station(name=name, code=code, zone=zone, 
                     interchange=interchange, lines=lines)
    self.stations[code] = station
```

### Adding New Services

```python
new_service = Service(
    service_id="VIC_NB",
    line="Victoria",
    direction="Northbound",
    stations=["VIC", "GPK", "OXC", "WST", "KGX"]
)
self.services["VIC_NB"] = new_service
```

### Generating Trains

```python
# Generate trains with 3-minute frequency
for i in range(20):
    departure_time = base_time + timedelta(minutes=i * 3)
    self._create_train(f"V{i:03d}", "VIC_NB", departure_time, 2)
```

## API Reference

### LondonUndergroundTimetable Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `get_station(code)` | Get station by code | code: str | Optional[Station] |
| `find_station_by_name(name)` | Find station by name | name: str | Optional[Station] |
| `get_next_trains(station, line, count, after_time)` | Get next departing trains | station: str, line: Optional[str], count: int, after_time: Optional[datetime] | List[Tuple[Train, datetime]] |
| `get_journey_time(from, to, train_id)` | Calculate journey time | from: str, to: str, train_id: str | Optional[timedelta] |
| `get_all_trains_on_line(line)` | Get trains on a line | line: str | List[Train] |
| `get_interchanges()` | Get interchange stations | - | List[Station] |
| `print_station_info(code)` | Display station info | code: str | None |
| `print_next_departures(code, line)` | Display departure board | code: str, line: Optional[str] | None |

## Testing

Run the built-in demonstration:

```bash
python3 london_underground_timetable.py
```

This will display:
- Network statistics
- Station information examples
- Next departure queries
- Interchange station list
- Journey time calculations

## Network Coverage

Current implementation includes:

- **21 Stations** across Zone 1-3
- **14 Interchange Stations**
- **4 Line Services** (with bidirectional routes)
- **90 Scheduled Trains** (generated for demonstration)

## Performance

- **Station lookup**: O(1) using dictionary
- **Train search**: O(n) where n = number of trains
- **Next departures**: O(n log n) due to sorting

## Future Enhancements

Possible extensions to the system:

1. **Real-time Updates**: Integration with TfL API for live data
2. **Delay Management**: Track and display service disruptions
3. **Route Planning**: Multi-leg journey planning with interchanges
4. **Zone-based Pricing**: Calculate fares based on zones
5. **Peak/Off-peak**: Different schedules for peak and off-peak times
6. **Weekend Services**: Alternative timetables for weekends
7. **Database Backend**: Persistent storage for schedules
8. **Web Interface**: REST API and web UI for queries

## License

This is a demonstration implementation created for educational purposes.

## Contributing

To add more stations or lines:

1. Add stations using `_add_station()` in `_initialize_network()`
2. Create services using `Service` dataclass
3. Generate trains using `_create_train()` method
4. Update documentation with new routes

## Author

Created as a comprehensive solution for London Underground timetable management.
