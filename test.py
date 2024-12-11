
from collections import UserDict
from datetime import *



class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if len(value) <= 1:
            raise ValueError("Ім'я не може бути менше 1 букви")
        super().__init__(value)
        
class Phone(Field):
    def __init__(self, value):
        if len(value) != 10:
            raise ValueError("Невірна довжина номера")
        elif not value.isdigit():
            raise ValueError('Введіть лише цифри')
        super().__init__(value)

        
class Birthday(Field):
    def __init__(self, value):
        try: 
            self.data = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self,phone):
        self.phones.append(Phone(phone))
        
    def add_birthday(self,birthday):
        self.birthday = Birthday(birthday)
        
    def find_phone(self,user_phone):
        for phone in self.phones:
            if phone.value == user_phone:
                return phone

    def edit_phone(self,old_phone, new_phone):
        
        for phone in self.phones:  
            if phone.value == old_phone:
                self.phones.append(Phone(new_phone))
                self.phones.remove(phone)
                return
        raise ValueError('Відсутній телефон')
                
            
    def remove_phone(self,remove):
        for phone in self.phones:  
            if phone.value == remove:
                self.phones.remove(phone)
                break
    
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)},birthday {self.birthday}"

class AddressBook(UserDict):
    
    def add_record(self,rec):
        self.data[rec.name.value] = rec

    def find(self,obj):
        return self.data.get(obj)
    
    def delete(self,user):
        return self.data.pop(user)
    
    def find_next_weekday(start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)
    
    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = datetime.today().date()

        for user in self.data.values():
            birthday_this_year = user.birthday.data.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
    
            if 0 <= (birthday_this_year - today).days <= days:
                if birthday_this_year.weekday() >= 5:
                    birthday_this_year = self.find_next_weekday(birthday_this_year,0)
                    

                congratulation_date_str = birthday_this_year.strftime("%Y.%m.%d")
                upcoming_birthdays.append({"name": user.name.value, "congratulation_date": congratulation_date_str})
        return upcoming_birthdays

    def __str__(self):
        return '\n'.join([str(x) for x in self.data.values()])

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "User not found"
        except ValueError as e:
            return e  # "Incorrect value. Please check and try again."
        except IndexError:
            return "Enter correct information."
    return inner


# Додавання контактів
# @input_error
def add_contact(args, book=None):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message



# Зміна контактів
def change_contact(args, book:AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
    else:
        raise KeyError

# # Виведення контакту
def show_phone(args, book = None):
    name = args[0]
    record = book.find(name)
    if record:
        return "; ".join([str(phone) for phone in record.phones])
    else:
        return KeyError

# Вивід всіх контактів
def all(book):
    return "\n".join([str(record) for record in book.data.values()])

def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        raise KeyError

def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    return str(record.birthday)

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd,*args

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip().lower()
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good buy!")
            break
        elif command == "hello":
            print("How can i help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(all(book))
        else:
            print("Invalid command.")



if __name__ == '__main__':
    main()