from DoAnCuoiKy.models.Employee import Employee


class Manager(Employee):
    def __init__(self,EmployeeId, EmployeeName, UserName, Password):
        super().__init__(EmployeeId,EmployeeName,UserName,Password)#kế thừa từ class Employee
    def __str__(self):
        return f"{self.EmployeeId}\t{self.EmployeeName}"
