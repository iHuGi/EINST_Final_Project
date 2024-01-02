"""
Projeto número 3, baseado no enunciado 2.

Por motivos de tempo este projeto não terá um GUI mas terá tudo o resto, como reservar os seats, 
não deixar reservar seats se já tiver reservado e também dar para cancelar os lugares. O projeto também não
terá um MENU em que o user possa simplesmente inserir os lugares. Eu queria fazer algo muito mais complexo até com
base de dados em PostgreSQL em que teriamos várias tabelas relacionais, com dados dos users, dados de faturação etc.
Porém não consigo fazer estas implementações no tempo adequado, seria usado SQL Alchemy, PostgreSQL e pg8000.

A classe main terá o código martelado das reservas com todo o código documentado para ser de fácil compreensão.

"""

class Theatre:
    class Seat:
        # Inner Seat class representing individual seats in the theatre
        def __init__(self, seat_number, price):
            self.seat_number = seat_number
            self.price = price
            self.reserved = False

        def compare(self, other_seat):
            # Comparison function for sorting seats
            # Compare seat numbers in a case-insensitive manner for sorting.
            # Returns 1 if self is greater, -1 if other_seat is greater, and 0 if equal.

            """
            If the first comparison is True, it becomes 1 - 0 (resulting in 1).
            If the first comparison is False, it becomes 0 - 1 (resulting in -1).
            If both comparisons are True or both are False, it becomes 1 - 1 or 0 - 0 (resulting in 0).
            """
            return (self.seat_number > other_seat.get_seat_number()) - (self.seat_number < other_seat.get_seat_number())

        def reserve(self):
            # Reserve the seat if it's not already reserved
            if not self.reserved:
                self.reserved = True
                print("Seat", self.seat_number, "reserved")
                return True
            else:
                return False

        def cancel(self):
            # Cancel reservation for the seat
            if self.reserved:
                self.reserved = False
                print("Reservation of seat", self.seat_number, "cancelled")
                return True
            else:
                return False

        def get_seat_number(self):
            return self.seat_number

        def get_price(self):
            return self.price

    def __init__(self, theatre_name, num_rows, seats_per_row):
        # Theatre class representing the overall theatre structure
        self.theatre_name = theatre_name
        self.seats = []
        # Loop to iterate over rows using ASCII values, For example, if num_rows is 8, the loop will iterate over the values 65, 66, ..., 72, 
        # which correspond to the ASCII values of 'A' to 'H'.
        for row in range(ord('A'), ord('A') + num_rows):
            print(row) # Debug 
            # Loop to iterate over seat numbers within each row
            for seat_num in range(1, seats_per_row + 1):
                print(seat_num) # Debug
                # Setting prices based on certain conditions
                price = 12.00
                if 'A' <= chr(row) < 'D' and 4 <= seat_num <= 9:
                # If the row is 'A', 'B', or 'C' and seat number is between 4 and 9, set a higher price
                    price = 14.00
                elif chr(row) > 'F' or seat_num < 4 or seat_num > 9:
                # If the row is after 'F' or seat number is less than 4 or greater than 9, set a lower price
                    price = 7.00
                # Creating Seat objects and adding them to the list of seats
                seat = self.Seat(chr(row) + "{:02d}".format(seat_num), price)
                self.seats.append(seat)

    def get_seats(self):
        return self.seats

    def reserve_seat(self, seat_number):
    # Reserving a seat using binary search
    # Create a Seat object representing the requested seat with a dummy price
        requested_seat = self.Seat(seat_number, 0)
    # Use binary search to find the requested seat in the list of seats
        found_seat = self.binary_search(requested_seat)
        if found_seat >= 0:
        # If the seat is found, attempt to reserve it
            return self.seats[found_seat].reserve()
        else:
        # If the seat is not found, print a message indicating that there is no such seat
            print("There is no seat", seat_number)
            return False

    def binary_search(self, requested_seat):
    # Binary search algorithm for finding a seat
        low = 0
        high = len(self.seats) - 1

        while low <= high:
            mid = (low + high) // 2  # Calculate the middle index
            mid_val = self.seats[mid]  # Get the seat at the middle index
            cmp = requested_seat.compare(mid_val)  # Compare the requested seat with the middle seat

            if cmp < 0:
            # If the requested seat comes before the middle seat, update the High index
                high = mid - 1
            elif cmp > 0:
            # If the requested seat comes after the middle seat, update the Low index
                low = mid + 1
            else:
            # If the requested seat matches the middle seat, return the index of the found seat
                return mid

    # If the loop exits without finding the seat, return -1
        return -1

class Main:
    @staticmethod
    def print_list(seat_list, message=""):
        for seat in seat_list:
            print(f"{seat.get_seat_number()} ${seat.get_price()}", end=" ")
        print()
        print(message)

    @staticmethod
    def main():
        # Main class for running the script
        theatre = Theatre("Olympian", 8, 12)

        # Trying to cancel a seat that is not reserved
        seat_D09 = next(seat for seat in theatre.get_seats() if seat.get_seat_number() == "D09")
        if not seat_D09.cancel():
            print("Seat is not reserved")
        
        # Another way to cancel a SEAT:
        # Finding the seat instance with seat number "A10"
        seat_A10 = next(seat for seat in theatre.get_seats() if seat.get_seat_number() == "A10")
        # Checking if the seat is reserved and canceling it, in this case cancel won't work because it is not reserved
        if seat_A10 is not None and seat_A10.cancel():
            print("Seat canceled successfully")
        else:
            print("Seat is not reserved or could not be canceled")

        # Reserve SEAT D09
        if theatre.reserve_seat("D09"):
            print("Please pay for D09")
        else:
            print("Seat already reserved")

       # Cancelling D09, it should work now since it is reserved
        seat_D09 = next((seat for seat in theatre.get_seats() if seat.get_seat_number() == "D09"), None)
        # Checking if the seat is reserved and canceling it
        if seat_D09 is not None and seat_D09.cancel():
            pass # If Cancelation is successful, we do nothing because the function already has a pre-defined message
        else:
            print("Seat is not reserved or could not be canceled")

        # Reserve SEAT D10
        if theatre.reserve_seat("D10"):
            print("Please pay for D10")
        else:
            print("Seat already reserved")

        # Reserve SEAT D11
        if theatre.reserve_seat("D11"):
            print("Please pay for D11")
        else:
            print("Seat already reserved")

        # Reserve SEAT D12
        if theatre.reserve_seat("D12"):
            print("Please pay for D12")
        else:
            print("Seat already reserved")

        # Try to reserve the SEAT again but find out that is not possible
        if theatre.reserve_seat("D12"):
            print("Please pay for D12")
        else:
            print("Seat already reserved")

        # Cancel reservation for SEAT D12 using the Seat's cancel method
        seat_d12 = next(seat for seat in theatre.get_seats() if seat.get_seat_number() == "D12")
        if not seat_d12.cancel():
            print("Seat is not reserved")

        # Reserve D12 again, by another person (maybe), in this case
        if theatre.reserve_seat("D12"):
            print("Please pay for D12")
        else:
            print("Seat already reserved")
            
        # Try to reserve a SEAT that does not EXIST
        if theatre.reserve_seat("B13"):
            print("Please pay for B13")
        
        # Trying to cancel a seat that is not reserved
        seat_F03 = next(seat for seat in theatre.get_seats() if seat.get_seat_number() == "F03")
        if not seat_F03.cancel():
            print("Seat is not reserved")

        print()

        # Reversing the order of seats and printing the reversed list
        print("\033[1mReversing the order of seats and printing the reversed list:\033[0m")
        reverse_seats = list(reversed(theatre.get_seats()))
        Main.print_list(reverse_seats)

        # Creating a new list of seats, adding two new seats with specified prices, and printing the list
        print("\033[1mCreating a new list of seats, adding two new seats with specified prices, and printing the list:\033[0m")
        price_seats = list(theatre.get_seats())
        price_seats.append(theatre.Seat("B00", 13.00))
        price_seats.append(theatre.Seat("A00", 13.00))
        Main.print_list(price_seats)

        # Sorting the list of seats based on the price using a lambda function and printing the sorted list
        print("\033[1mSorting the list of seats based on the price using a lambda function and printing the sorted list:\033[0m")
        price_seats.sort(key=lambda seat: seat.get_price())
        Main.print_list(price_seats)

if __name__ == "__main__":
    Main.main()
