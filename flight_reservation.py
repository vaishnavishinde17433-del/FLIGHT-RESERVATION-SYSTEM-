"""Flight Reservation System using Searching and Sorting (DSA Mini Project)"""
import random

# ---------------- Data ----------------
_raw = [
    (101, "IndiGo", "Pune", "Delhi", "06:15", 5200, 5),
    (102, "Air India", "Pune", "Mumbai", "09:30", 2100, 3),
    (103, "Vistara", "Pune", "Delhi", "14:45", 6100, 2),
    (104, "SpiceJet", "Mumbai", "Bengaluru", "07:50", 4300, 4),
    (105, "IndiGo", "Pune", "Delhi", "19:20", 4800, 6),
    (106, "Akasa Air", "Delhi", "Pune", "11:05", 5600, 1),
    (107, "Air India", "Pune", "Bengaluru", "16:10", 3900, 7),
]
KEYS = ("no", "airline", "src", "dst", "dep", "price", "seats")
FLIGHTS = [dict(zip(KEYS, row)) for row in _raw]
bookings = []
steps = {"count": 0}


# ---------------- Searching ----------------
def linear_search(flights, src, dst):
    """Find all flights matching source and destination. O(n)."""
    result = []
    for flight in flights:
        steps["count"] += 1
        if flight["src"].lower() == src.lower() and flight["dst"].lower() == dst.lower():
            result.append(flight)
    return result


def binary_search(sorted_flights, flight_no):
    """Search by flight number in sorted data. O(log n)."""
    low, high = 0, len(sorted_flights) - 1
    while low <= high:
        steps["count"] += 1
        mid = (low + high) // 2
        if sorted_flights[mid]["no"] == flight_no:
            return sorted_flights[mid]
        elif sorted_flights[mid]["no"] < flight_no:
            low = mid + 1
        else:
            high = mid - 1
    return None


# ---------------- Sorting ----------------
def merge_sort(arr, key):
    """Merge sort by a selected key. O(n log n)."""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        steps["count"] += 1
        if left[i][key] <= right[j][key]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def insertion_sort(arr, key):
    """Insertion sort by a selected key. O(n^2) worst case."""
    arr = arr[:]
    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        while j >= 0:
            steps["count"] += 1
            if arr[j][key] > current[key]:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = current
    return arr


# ---------------- Booking ----------------
def book_ticket(flights, flight_no, passenger):
    flight = binary_search(merge_sort(flights, "no"), flight_no)
    if flight is None:
        return "Flight not found."
    if flight["seats"] == 0:
        return "Sorry, no seats available."

    flight["seats"] -= 1
    pnr = "PNR" + str(random.randint(10000, 99999))
    bookings.append({"pnr": pnr, "name": passenger, "flight": flight_no})
    return f"Booking confirmed! {passenger}, Flight {flight_no}, {pnr}"


def show(flights):
    print(f"{'No':<5}{'Airline':<11}{'From':<8}{'To':<11}{'Dep':<7}{'Price':<7}{'Seats'}")
    for flight in flights:
        print(
            f"{flight['no']:<5}{flight['airline']:<11}{flight['src']:<8}"
            f"{flight['dst']:<11}{flight['dep']:<7}{flight['price']:<7}{flight['seats']}"
        )


# ---------------- Console demo ----------------
def demo():
    print("=== Pune to Delhi flights (Linear Search) ===")
    steps["count"] = 0
    found = linear_search(FLIGHTS, "Pune", "Delhi")
    show(found)
    print("Steps:", steps["count"])

    print("\n=== Sorted by price (Merge Sort) ===")
    steps["count"] = 0
    show(merge_sort(found, "price"))
    print("Steps:", steps["count"])

    print("\n=== Sorted by departure time (Insertion Sort) ===")
    steps["count"] = 0
    show(insertion_sort(found, "dep"))
    print("Steps:", steps["count"])

    print("\n=== Search flight 105 (Binary Search) ===")
    by_no = merge_sort(FLIGHTS, "no")
    steps["count"] = 0
    flight = binary_search(by_no, 105)
    if flight:
        print(
            "Found:", flight["airline"], flight["src"], "->", flight["dst"],
            "| Steps:", steps["count"]
        )
    else:
        print("Flight not found | Steps:", steps["count"])

    print("\n=== Booking ===")
    print(book_ticket(FLIGHTS, 105, "Trishala Sonawane"))
    booked_flight = binary_search(merge_sort(FLIGHTS, "no"), 105)
    if booked_flight:
        print("Seats left on flight 105:", booked_flight["seats"])


# ---------------- GUI (Tkinter) ----------------
def run_gui():
    import tkinter as tk
    from tkinter import ttk, messagebox

    root = tk.Tk()
    root.title("Flight Reservation System")
    root.geometry("900x520")

    top = tk.Frame(root)
    top.pack(pady=10)

    tk.Label(top, text="From:").grid(row=0, column=0)
    e_src = tk.Entry(top, width=12)
    e_src.grid(row=0, column=1, padx=5)

    tk.Label(top, text="To:").grid(row=0, column=2)
    e_dst = tk.Entry(top, width=12)
    e_dst.grid(row=0, column=3, padx=5)

    tk.Label(top, text="Sort by:").grid(row=0, column=4)
    sort_var = tk.StringVar(value="Price (Merge Sort)")
    options = ["Price (Merge Sort)", "Departure (Insertion Sort)"]
    ttk.Combobox(
        top, textvariable=sort_var, width=22, state="readonly", values=options
    ).grid(row=0, column=5, padx=5)

    cols = ("no", "airline", "src", "dst", "dep", "price", "seats")
    tree = ttk.Treeview(root, columns=cols, show="headings", height=12)
    for column in cols:
        tree.heading(column, text=column.upper())
        tree.column(column, width=110, anchor="center")
    tree.pack(padx=10, pady=5, fill="x")

    status = tk.Label(root, text="", fg="blue")
    status.pack()

    def fill(rows):
        tree.delete(*tree.get_children())
        for flight in rows:
            tree.insert("", "end", values=[flight[column] for column in cols])

    def do_search():
        steps["count"] = 0
        if e_src.get().strip() and e_dst.get().strip():
            rows = linear_search(FLIGHTS, e_src.get().strip(), e_dst.get().strip())
        else:
            rows = FLIGHTS[:]

        if sort_var.get().startswith("Price"):
            rows = merge_sort(rows, "price")
        else:
            rows = insertion_sort(rows, "dep")

        fill(rows)
        status.config(text=f"{len(rows)} flight(s) found | steps: {steps['count']}")

    def do_binary():
        number = fno.get().strip()
        if not number.isdigit():
            messagebox.showerror("Error", "Enter a numeric flight number")
            return

        steps["count"] = 0
        flight = binary_search(merge_sort(FLIGHTS, "no"), int(number))
        fill([flight] if flight else [])
        message = "Flight found" if flight else "Flight not found"
        status.config(text=message + f" | steps: {steps['count']}")

    def do_book():
        number = fno.get().strip()
        passenger = name.get().strip()
        if not number.isdigit() or not passenger:
            messagebox.showerror("Error", "Enter flight number and passenger name")
            return

        messagebox.showinfo("Booking", book_ticket(FLIGHTS, int(number), passenger))
        do_search()

    bar = tk.Frame(root)
    bar.pack(pady=10)

    tk.Button(bar, text="Search / Sort", command=do_search).grid(row=0, column=0, padx=5)
    tk.Label(bar, text="Flight No:").grid(row=0, column=1)
    fno = tk.Entry(bar, width=8)
    fno.grid(row=0, column=2, padx=5)
    tk.Button(bar, text="Binary Search", command=do_binary).grid(row=0, column=3, padx=5)
    tk.Label(bar, text="Passenger:").grid(row=0, column=4)
    name = tk.Entry(bar, width=16)
    name.grid(row=0, column=5, padx=5)
    tk.Button(bar, text="Book Ticket", command=do_book).grid(row=0, column=6, padx=5)

    do_search()
    root.mainloop()


if __name__ == "__main__":
    import sys
    demo() if "--demo" in sys.argv else run_gui()
