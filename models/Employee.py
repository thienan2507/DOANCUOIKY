class Employee:
    def __init__(self,EmployeeId, EmployeeName, UserName, Password):
        self.EmployeeId=EmployeeId
        self.EmployeeName=EmployeeName
        self.UserName=UserName
        self.Password=Password
    def __str__(self):
        return f"{self.EmployeeId}\t{self.EmployeeName}"