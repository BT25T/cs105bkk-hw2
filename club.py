"""HW2 · club.py: the club and its chat bot. Practises Session 4 (each class has one job),
Session 5 (importing your own modules and the standard library) and Session 6 (catching only
the errors you expect)."""

from errors import SignupError, UnknownEventError
from event import Event


class Club:
    """A student club. It finds events by title; each Event looks after its own seats."""

    def __init__(self, name: str):
        """Provided: a club with no events yet."""
        self.name = name
        self.events: dict[str, Event] = {}

    def add_event(self, title: str, capacity: int) -> Event:
        """Make a new Event, store it under its title, and return it."""
        if title in self.events.keys() or capacity <= 0:
            raise ValueError
        event = (Event(title, capacity))
        self.events[title] = event
        return event

    def event(self, title: str) -> Event:
        """Return the event with this title, or raise UnknownEventError."""
        for event in self.events.values():
            if event.title == title:
                return event
        raise UnknownEventError(title)

    def handle(self, line: str) -> str:
        """Answer one chat command, such as "join, Muay Thai basics, Nino", with one sentence."""
        _line = [item.strip() for item in line.split(",")]
        command = _line[0]
        if command not in ["join", "leave"] or len(_line) != 3:
            return f"Sorry, I don't understand '{command}'."
        title, member = _line[1], _line[2]
        try:
            event = self.event(title)
            if command == 'join':
                initial_seats = event.seats_left()
                event.sign_up(member)
                if initial_seats == 0:
                    return f"{member} is on the waitlist for {title}."
                return f"{member} has a seat at {title}."
    
            if command == 'leave':
                new_member = event.cancel(member)
                if new_member is None:
                    return f"{member} left {title}."
                return f"{member} left {title}. {new_member} gets the seat."

        except SignupError as e:
            return f"Sorry, {e}." 

    def attendance(self) -> dict[str, int]:
        """How many events each member has a seat at. The waitlist does not count."""
        member_list = {}
        for _, event in self.events.items():
            for member in event.seats:
                if member not in member_list:
                    member_list[member] = 1
                else:
                    member_list[member] += 1
        return member_list

if __name__ == "__main__":
    # Provided: a short run of the chat bot. It runs only with `python club.py`, not on import.
    club = Club("Harbour.Space Bangkok club")
    club.add_event("Muay Thai basics", 2)
    for line in [
        "join, Muay Thai basics, Nino",
        "join, Muay Thai basics, Aung",
        "join, Muay Thai basics, Tashi",
        "leave, Muay Thai basics, Nino",
        "join, Chess night, Ploy",
    ]:
        print(club.handle(line))
