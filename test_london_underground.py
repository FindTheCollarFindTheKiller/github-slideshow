"""
Test suite for London Underground Timetable System

This file contains unit tests to validate the functionality of the
London Underground timetable system.
"""

import unittest
from datetime import datetime, timedelta
from london_underground_timetable import (
    Station, Service, ScheduledStop, Train,
    LondonUndergroundTimetable, LineColor
)


class TestStation(unittest.TestCase):
    """Test cases for Station class"""
    
    def test_station_creation(self):
        """Test creating a station"""
        station = Station(
            name="Oxford Circus",
            code="OXC",
            zone=1,
            interchange=True,
            lines=["Central", "Victoria", "Bakerloo"]
        )
        self.assertEqual(station.name, "Oxford Circus")
        self.assertEqual(station.code, "OXC")
        self.assertEqual(station.zone, 1)
        self.assertTrue(station.interchange)
        self.assertEqual(len(station.lines), 3)
    
    def test_station_str(self):
        """Test station string representation"""
        station = Station("Bank", "BNK", 1)
        self.assertIn("Bank", str(station))
        self.assertIn("Zone 1", str(station))
    
    def test_station_repr(self):
        """Test station repr"""
        station = Station("Bank", "BNK", 1)
        repr_str = repr(station)
        self.assertIn("Station", repr_str)
        self.assertIn("BNK", repr_str)


class TestService(unittest.TestCase):
    """Test cases for Service class"""
    
    def test_service_creation(self):
        """Test creating a service"""
        service = Service(
            service_id="CEN_EB",
            line="Central",
            direction="Eastbound",
            stations=["OXC", "TCR", "BNK"]
        )
        self.assertEqual(service.service_id, "CEN_EB")
        self.assertEqual(service.line, "Central")
        self.assertEqual(len(service.stations), 3)
    
    def test_service_str(self):
        """Test service string representation"""
        service = Service("CEN_EB", "Central", "Eastbound", ["OXC", "TCR"])
        service_str = str(service)
        self.assertIn("Central", service_str)
        self.assertIn("Eastbound", service_str)


class TestScheduledStop(unittest.TestCase):
    """Test cases for ScheduledStop class"""
    
    def test_scheduled_stop_creation(self):
        """Test creating a scheduled stop"""
        now = datetime.now()
        later = now + timedelta(minutes=1)
        stop = ScheduledStop(
            station_code="OXC",
            arrival_time=now,
            departure_time=later,
            platform="1"
        )
        self.assertEqual(stop.station_code, "OXC")
        self.assertEqual(stop.arrival_time, now)
        self.assertEqual(stop.departure_time, later)
        self.assertEqual(stop.platform, "1")


class TestTrain(unittest.TestCase):
    """Test cases for Train class"""
    
    def setUp(self):
        """Set up test data"""
        self.service = Service(
            service_id="CEN_EB",
            line="Central",
            direction="Eastbound",
            stations=["OXC", "TCR", "BNK"]
        )
        
        now = datetime.now()
        self.stops = [
            ScheduledStop("OXC", now, now + timedelta(minutes=1)),
            ScheduledStop("TCR", now + timedelta(minutes=3), now + timedelta(minutes=4)),
            ScheduledStop("BNK", now + timedelta(minutes=6), now + timedelta(minutes=7))
        ]
        
        self.train = Train(
            train_id="CE001",
            service=self.service,
            stops=self.stops,
            operating=True
        )
    
    def test_train_creation(self):
        """Test creating a train"""
        self.assertEqual(self.train.train_id, "CE001")
        self.assertEqual(len(self.train.stops), 3)
        self.assertTrue(self.train.operating)
    
    def test_get_departure_time(self):
        """Test getting departure time from a station"""
        dep_time = self.train.get_departure_time("OXC")
        self.assertIsNotNone(dep_time)
        self.assertEqual(dep_time, self.stops[0].departure_time)
    
    def test_get_departure_time_not_found(self):
        """Test getting departure time for non-existent station"""
        dep_time = self.train.get_departure_time("XXX")
        self.assertIsNone(dep_time)
    
    def test_get_arrival_time(self):
        """Test getting arrival time at a station"""
        arr_time = self.train.get_arrival_time("BNK")
        self.assertIsNotNone(arr_time)
        self.assertEqual(arr_time, self.stops[2].arrival_time)
    
    def test_get_arrival_time_not_found(self):
        """Test getting arrival time for non-existent station"""
        arr_time = self.train.get_arrival_time("XXX")
        self.assertIsNone(arr_time)


class TestLondonUndergroundTimetable(unittest.TestCase):
    """Test cases for LondonUndergroundTimetable class"""
    
    def setUp(self):
        """Set up timetable for testing"""
        self.timetable = LondonUndergroundTimetable()
    
    def test_timetable_initialization(self):
        """Test that timetable initializes with data"""
        self.assertGreater(len(self.timetable.stations), 0)
        self.assertGreater(len(self.timetable.services), 0)
        self.assertGreater(len(self.timetable.trains), 0)
    
    def test_get_station(self):
        """Test getting a station by code"""
        station = self.timetable.get_station("OXC")
        self.assertIsNotNone(station)
        self.assertEqual(station.name, "Oxford Circus")
        self.assertEqual(station.code, "OXC")
    
    def test_get_station_not_found(self):
        """Test getting a non-existent station"""
        station = self.timetable.get_station("XXX")
        self.assertIsNone(station)
    
    def test_find_station_by_name(self):
        """Test finding a station by name"""
        station = self.timetable.find_station_by_name("Bank")
        self.assertIsNotNone(station)
        self.assertEqual(station.code, "BNK")
    
    def test_find_station_by_name_case_insensitive(self):
        """Test finding station by name is case insensitive"""
        station = self.timetable.find_station_by_name("BANK")
        self.assertIsNotNone(station)
        self.assertEqual(station.code, "BNK")
    
    def test_find_station_by_name_not_found(self):
        """Test finding non-existent station by name"""
        station = self.timetable.find_station_by_name("Nonexistent Station")
        self.assertIsNone(station)
    
    def test_get_interchanges(self):
        """Test getting all interchange stations"""
        interchanges = self.timetable.get_interchanges()
        self.assertGreater(len(interchanges), 0)
        for station in interchanges:
            self.assertTrue(station.interchange)
    
    def test_get_all_trains_on_line(self):
        """Test getting all trains on a specific line"""
        central_trains = self.timetable.get_all_trains_on_line("Central")
        self.assertGreater(len(central_trains), 0)
        for train in central_trains:
            self.assertEqual(train.service.line, "Central")
    
    def test_get_all_trains_on_line_not_found(self):
        """Test getting trains on non-existent line"""
        trains = self.timetable.get_all_trains_on_line("NonexistentLine")
        self.assertEqual(len(trains), 0)
    
    def test_get_next_trains(self):
        """Test getting next trains from a station"""
        # Use a time far in the past to ensure we get results
        past_time = datetime.now().replace(hour=5, minute=0)
        departures = self.timetable.get_next_trains("OXC", count=5, after_time=past_time)
        self.assertGreater(len(departures), 0)
        self.assertLessEqual(len(departures), 5)
        
        # Verify departures are sorted by time
        times = [dep[1] for dep in departures]
        self.assertEqual(times, sorted(times))
    
    def test_get_next_trains_with_line_filter(self):
        """Test getting next trains filtered by line"""
        past_time = datetime.now().replace(hour=5, minute=0)
        departures = self.timetable.get_next_trains(
            "OXC", line="Central", count=5, after_time=past_time
        )
        for train, _ in departures:
            self.assertEqual(train.service.line, "Central")
    
    def test_get_journey_time(self):
        """Test calculating journey time"""
        # Get a train and test journey time between its first and last stops
        train = self.timetable.trains[0]
        if len(train.stops) >= 2:
            from_station = train.stops[0].station_code
            to_station = train.stops[-1].station_code
            journey_time = self.timetable.get_journey_time(
                from_station, to_station, train.train_id
            )
            self.assertIsNotNone(journey_time)
            self.assertGreater(journey_time.total_seconds(), 0)
    
    def test_get_journey_time_invalid_train(self):
        """Test journey time with invalid train ID"""
        journey_time = self.timetable.get_journey_time("OXC", "BNK", "INVALID")
        self.assertIsNone(journey_time)
    
    def test_get_journey_time_invalid_stations(self):
        """Test journey time with stations not on the train route"""
        train = self.timetable.trains[0]
        journey_time = self.timetable.get_journey_time("XXX", "YYY", train.train_id)
        self.assertIsNone(journey_time)
    
    def test_stations_have_valid_zones(self):
        """Test that all stations have valid zone numbers"""
        for station in self.timetable.stations.values():
            self.assertGreaterEqual(station.zone, 1)
            self.assertLessEqual(station.zone, 9)
    
    def test_stations_have_lines(self):
        """Test that all stations have at least one line"""
        for station in self.timetable.stations.values():
            self.assertGreater(len(station.lines), 0)
    
    def test_interchange_stations_have_multiple_lines(self):
        """Test that interchange stations have multiple lines"""
        for station in self.timetable.get_interchanges():
            self.assertGreater(len(station.lines), 1)
    
    def test_trains_have_valid_services(self):
        """Test that all trains have valid services"""
        for train in self.timetable.trains:
            self.assertIn(train.service.service_id, self.timetable.services)
    
    def test_trains_have_stops(self):
        """Test that all trains have at least one stop"""
        for train in self.timetable.trains:
            self.assertGreater(len(train.stops), 0)
    
    def test_train_stops_are_sequential(self):
        """Test that train stops are in chronological order"""
        for train in self.timetable.trains:
            for i in range(len(train.stops) - 1):
                current_stop = train.stops[i]
                next_stop = train.stops[i + 1]
                self.assertLessEqual(
                    current_stop.departure_time,
                    next_stop.arrival_time
                )


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def setUp(self):
        """Set up timetable for testing"""
        self.timetable = LondonUndergroundTimetable()
    
    def test_complete_journey_workflow(self):
        """Test a complete journey planning workflow"""
        # Find a station
        station = self.timetable.find_station_by_name("Oxford Circus")
        self.assertIsNotNone(station)
        
        # Get next trains from that station
        past_time = datetime.now().replace(hour=5, minute=0)
        departures = self.timetable.get_next_trains(
            station.code, count=3, after_time=past_time
        )
        self.assertGreater(len(departures), 0)
        
        # Get information about the first train
        train, departure_time = departures[0]
        self.assertIsNotNone(train)
        self.assertIsNotNone(departure_time)
        
        # Check the train has a valid service
        self.assertIsNotNone(train.service)
        self.assertGreater(len(train.service.stations), 0)
    
    def test_line_coverage(self):
        """Test that the system covers multiple lines"""
        lines_covered = set()
        for train in self.timetable.trains:
            lines_covered.add(train.service.line)
        
        # Should have at least 2 lines implemented
        self.assertGreaterEqual(len(lines_covered), 2)
    
    def test_bidirectional_services(self):
        """Test that lines have services in both directions"""
        services_by_line = {}
        for service in self.timetable.services.values():
            if service.line not in services_by_line:
                services_by_line[service.line] = set()
            services_by_line[service.line].add(service.direction)
        
        # At least one line should have bidirectional service
        bidirectional_lines = [
            line for line, directions in services_by_line.items()
            if len(directions) >= 2
        ]
        self.assertGreater(len(bidirectional_lines), 0)


def run_tests():
    """Run all tests and display results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestStation))
    suite.addTests(loader.loadTestsFromTestCase(TestService))
    suite.addTests(loader.loadTestsFromTestCase(TestScheduledStop))
    suite.addTests(loader.loadTestsFromTestCase(TestTrain))
    suite.addTests(loader.loadTestsFromTestCase(TestLondonUndergroundTimetable))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
