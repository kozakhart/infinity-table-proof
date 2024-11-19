from employees_pb2 import Employee, Employees
import os
# Create and serialize protobuf message
employee1 = Employee(id=1, name="John Doe", salary=50000.0)
employee2 = Employee(id=2, name="Jane Doe", salary=60000.0)

employees = Employees(employee=[employee1, employee2])
serialized_data = employees.SerializeToString()

# Write the serialized data to a binary file
file_path = os.path.join(os.getcwd(), "employees.bin")

# Serialize the Employees message
with open(file_path, "wb") as f:
    f.write(employees.SerializeToString())

print(f"File saved at: {file_path}")
