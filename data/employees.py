import random
from faker import Faker

fake = Faker()

def generate_employee_data(num_employees=10):
    departments = ['Engineering', 'Marketing', 'Sales', 'HR', 'Finance']
    
    employees = []
    for _ in range(num_employees):
        employees.append({
            "employee_id": fake.uuid4(),
            "name": fake.name(),
            "department": random.choice(departments),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address": fake.address().replace("\n", ", "),
            "job_title": fake.job(),
            "start_date": str(fake.date_this_decade()),
            "salary": random.randint(50000, 150000)
        })
        
    return employees