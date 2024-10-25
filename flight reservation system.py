import heapq

class Flight:
    def __init__(self, flight_number, departure, destination, duration, airline):
        self.flight_number = flight_number
        self.departure = departure
        self.destination = destination
        self.duration = duration
        self.airline = airline

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)
        self.edges[value] = []

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append((to_node, distance))
        self.edges[to_node].append((from_node, distance))
        self.distances[(from_node, to_node)] = distance
        self.distances[(to_node, from_node)] = distance

    def dijkstra(self, initial):
        visited = {initial: 0}
        path = {}

        nodes = set(self.nodes)

        while nodes:
            min_node = None
            for node in nodes:
                if node in visited:
                    if min_node is None:
                        min_node = node
                    elif visited[node] < visited[min_node]:
                        min_node = node

            if min_node is None:
                break

            nodes.remove(min_node)
            current_weight = visited[min_node]

            for edge in self.edges[min_node]:
                weight = current_weight + self.distances[(min_node, edge[0])]
                if edge[0] not in visited or weight < visited[edge[0]]:
                    visited[edge[0]] = weight
                    path[edge[0]] = min_node

        return visited, path

class ReservationSystem:
    def __init__(self):
        self.graph = Graph()
        self.flights = {}
        self.reservations = {}

    def add_airport(self, airport_code):
        self.graph.add_node(airport_code.upper())

    def add_flight(self, flight_number, departure, destination, duration, airline):
        flight = Flight(flight_number, departure.upper(), destination.upper(), duration, airline)
        self.flights[flight_number] = flight
        self.graph.add_edge(departure.upper(), destination.upper(), duration)

    def search_flights(self, from_airport, to_airport, preferred_airline=None):
        from_airport = from_airport.upper()
        to_airport = to_airport.upper()
        distances, paths = self.graph.dijkstra(from_airport)
        route = []
        current_location = to_airport

        while current_location != from_airport:
            try:
                route.insert(0, current_location)
                current_location = paths[current_location]
            except KeyError:
                return None, None

        route.insert(0, from_airport)

        # Collect airlines on the route
        available_airlines = set()
        for flight in self.flights.values():
            if flight.departure in route and flight.destination in route:
                available_airlines.add(flight.airline)

        if preferred_airline and preferred_airline not in available_airlines:
            return None, None

        return route, distances[to_airport], list(available_airlines)

    def book_ticket(self, user, from_airport, to_airport, travel_date, preferred_airline=None):
        route, duration, available_airlines = self.search_flights(from_airport, to_airport, preferred_airline)
        
        if route is None:
            print("Route not possible or no available flight with the preferred airline.")
            return None
        
        reservation_id = len(self.reservations) + 1
        airline = preferred_airline if preferred_airline else ", ".join(available_airlines)
        self.reservations[reservation_id] = {
            "user": user,
            "route": route,
            "duration": duration,
            "date": travel_date,
            "airline": airline
        }
        return reservation_id

    def manage_reservation(self, reservation_id):
        if reservation_id in self.reservations:
            return self.reservations[reservation_id]
        else:
            return None

# Example usage with user input
if __name__ == "__main__":
    system = ReservationSystem()
    
    # Adding Indian airports and flights
    system.add_airport("DEL")  # Indira Gandhi International Airport, New Delhi
    system.add_airport("BOM")  # Chhatrapati Shivaji Maharaj International Airport, Mumbai
    system.add_airport("BLR")  # Kempegowda International Airport, Bengaluru
    system.add_airport("HYD")  # Rajiv Gandhi International Airport, Hyderabad
    system.add_airport("MAA")  # Chennai International Airport, Chennai

    system.add_flight("AI101", "DEL", "BOM", 2, "Air India")
    system.add_flight("SG202", "DEL", "BLR", 2.5, "SpiceJet")
    system.add_flight("6E303", "BOM", "HYD", 1.5, "IndiGo")
    system.add_flight("UK404", "BLR", "MAA", 1, "Vistara")
    system.add_flight("G8505", "HYD", "MAA", 1.5, "GoAir")

    # Take user inputs
    user_name = input("Enter your name: ")
    from_airport = input("Enter starting airport code (e.g., DEL): ")
    to_airport = input("Enter destination airport code (e.g., BOM): ")
    travel_date = input("Enter your travel date (YYYY-MM-DD): ")
    preferred_airline = input("Enter preferred airline (or press enter to skip): ")

    # Book a ticket
    reservation_id = system.book_ticket(user_name, from_airport, to_airport, travel_date, preferred_airline)
    
    if reservation_id:
        print(f"Reservation successful! Reservation ID: {reservation_id}")
        reservation = system.manage_reservation(reservation_id)
        print("Reservation Details:", reservation)
    else:
        print("Booking failed. Please try again.")
