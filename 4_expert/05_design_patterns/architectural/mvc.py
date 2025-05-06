"""
MVC (Model-View-Controller) Architectural Pattern

The MVC pattern divides an application into three interconnected components:
1. Model: Manages data, logic and rules of the application
2. View: Visual representation of the Model (UI)
3. Controller: Accepts input and converts it to commands for the Model or View

This pattern is widely used in web applications and GUI frameworks.
"""

# Model component - Represents and manages the data
class StudentModel:
    def __init__(self):
        self.student_id = None
        self.name = None
        self.grade = None
        
    def get_id(self):
        return self.student_id
        
    def set_id(self, student_id):
        self.student_id = student_id
        
    def get_name(self):
        return self.name
        
    def set_name(self, name):
        self.name = name
        
    def get_grade(self):
        return self.grade
        
    def set_grade(self, grade):
        self.grade = grade


# View component - Responsible for rendering the UI
class StudentView:
    def show_student_details(self, student_id, student_name, student_grade):
        print("\n===== Student Details =====")
        print(f"ID: {student_id}")
        print(f"Name: {student_name}")
        print(f"Grade: {student_grade}")
        print("==========================")
        
    def show_error_message(self, message):
        print(f"\nError: {message}")


# Controller component - Handles user interaction and updates model/view
class StudentController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    def set_student_details(self, student_id, name, grade):
        try:
            self.model.set_id(student_id)
            self.model.set_name(name)
            self.model.set_grade(grade)
        except Exception as e:
            self.view.show_error_message(str(e))
    
    def update_student_grade(self, grade):
        try:
            self.model.set_grade(grade)
        except Exception as e:
            self.view.show_error_message(str(e))
    
    def view_student_details(self):
        try:
            student_id = self.model.get_id()
            student_name = self.model.get_name()
            student_grade = self.model.get_grade()
            self.view.show_student_details(student_id, student_name, student_grade)
        except Exception as e:
            self.view.show_error_message(str(e))


# Example usage
if __name__ == "__main__":
    # Create MVC components
    model = StudentModel()
    view = StudentView()
    controller = StudentController(model, view)
    
    # Set initial student details
    controller.set_student_details(1001, "John Smith", "A")
    
    # Display student information
    controller.view_student_details()
    
    # Update student grade
    controller.update_student_grade("A+")
    
    # Display updated student information
    controller.view_student_details()