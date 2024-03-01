from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
from colors import color

file_name = 'register_file.txt'
file_name2 = 'register2_file.txt'

'''
Register format: 
    -> Keys: name do membro
    -> Values: lista [telephone, entry_date, final_date, plataforma de pagamento]

entry_date: member's entry date
final_date: date which member must leave 

OBS: final_date will be updated when a admin notifies that a payment has been received.
'''

class Member():
    def __init__(self, name: str, telephone: str, entry_date: str, final_date: str, payment_plataform: str):
        self.name = name
        self.telephone = telephone
        self.entry_date = datetime.strptime(entry_date, "%d/%m/%Y")   
        self.final_date = datetime.strptime(final_date, "%d/%m/%Y") 
        self.payment_plataform = payment_plataform

    def update_final_date(self):
        self.final_date = self.final_date + relativedelta(months=1)


class Register():
    def __init__(self):
        self.members = {}

    def add_member(self, member: Member):
        self.members[member.name] = member
    
    def remove_member(self, name):
        self.members.pop(name)
        
    def show_members(self):
        message = ""
        for member_name, member in self.members.items():
            message += f"Member Name: {member_name}\n"
            message += f"Telephone: {member.telephone}\n"
            message += f"Entry Date: {member.entry_date.strftime('%d/%m/%Y')}\n"
            message += f"Final Date: {member.final_date.strftime('%d/%m/%Y')}\n"
            message += f"Payment Platform: {member.payment_plataform}\n"
            message += "=================\n\n"

        
        return message
    
    def return_member(self, name):
        return self.members[name]
    
    def get_register(self, file_name):
        self.members = {}
        file_text = ""
        
        with open(file_name, "r") as file:
            # Read the entire contents of the file
            file_text = file.read()

        members = file_text.split("\n")

        for member in members: 
            if member != '':
                re.findall(r"'([^']*)'", member)
                name, telephone, entry_date, final_date, payment_plataform = re.findall(r"'([^']*)'", member)
                self.members[name] = Member(name, telephone, entry_date, final_date, payment_plataform)

    def set_register(self, file_path):
        message = ""
        for name, member in self.members.items():
            entry_data = member.entry_date.strftime("%d/%m/%Y")
            final_data = member.final_date.strftime("%d/%m/%Y")
            message += f"['{member.name}', '{member.telephone}', '{entry_data}', '{final_data}', '{member.payment_plataform}']\n"

        with open(file_path, "w") as file:
            # Write to the file
            file.write(message)
            
        






