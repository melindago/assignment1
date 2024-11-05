import re

class StyleChecker:
    def __init__(self, file_path):
        self.file_path = file_path
        self.report_data = {}

    def read_file(self):
        with open(self.file_path, 'r') as file:
            self.lines = file.readlines()

    def file_structure(self):
        self.report_data['Total Lines'] = len(self.lines)

    def find_imports(self):
        imports = []
        for line in self.lines:
            line = line.strip()
            if line.startswith("import") or line.startswith("from"):
                imports.append(line)
        self.report_data['Imports'] = imports

    def find_classes(self):
        classes = []
        for line in self.lines:
            line = line.strip()
            if line.startswith("class "):
                class_name = line.split()[1].split('(')[0]
                classes.append(class_name)
        self.report_data['Classes'] = classes

    def find_functions(self):
        functions = []
        inside_class = False
        for line in self.lines:
            line = line.strip()
            if line.startswith("class "):
                inside_class = True
            elif line.startswith("def "):
                function_name = line.split()[1].split('(')[0]
                if not inside_class:
                    functions.append(function_name)
            if line == "":
                inside_class = False
        self.report_data['Functions'] = functions

    def check_docstrings(self):
        docstrings = []
        current_class = None
        for i, line in enumerate(self.lines):
            line = line.strip()
            if line.startswith("class "):
                class_name = line.split()[1].split('(')[0]
                current_class = class_name
                if i + 1 < len(self.lines) and self.lines[i + 1].strip().startswith('"""'):
                    docstring = self.lines[i + 1].strip()
                    docstrings.append(f"Class {class_name}: {docstring}")
                else:
                    docstrings.append(f"Class {class_name}: DocString not found")
            elif line.startswith("def "):
                function_name = line.split()[1].split('(')[0]
                if i + 1 < len(self.lines) and self.lines[i + 1].strip().startswith('"""'):
                    docstring = self.lines[i + 1].strip()
                    if current_class:
                        docstrings.append(f"Method {function_name} in {current_class}: {docstring}")
                    else:
                        docstrings.append(f"Function {function_name}: {docstring}")
                else:
                    if current_class:
                        docstrings.append(f"Method {function_name} in {current_class}: DocString not found")
                    else:
                        docstrings.append(f"Function {function_name}: DocString not found")
        self.report_data['DocStrings'] = docstrings

    def check_type_annotations(self):
        missing_annotations = []
        for line in self.lines:
            line = line.strip()
            if line.startswith("def "):
                if '->' not in line and ':' not in line.split('(', 1)[1]:
                    function_name = line.split()[1].split('(')[0]
                    missing_annotations.append(function_name)
        if missing_annotations:
            self.report_data['Missing Type Annotations'] = missing_annotations
        else:
            self.report_data['Missing Type Annotations'] = ["All functions and methods use type annotations"]

    def check_naming_conventions(self):
        camel_case = re.compile(r'^[A-Z][a-zA-Z0-9]+$')
        snake_case = re.compile(r'^[a-z_][a-z0-9_]*$')
        non_compliant_classes = []
        non_compliant_functions = []
        
        for line in self.lines:
            line = line.strip()
            if line.startswith("class "):
                class_name = line.split()[1].split('(')[0]
                if not camel_case.match(class_name):
                    non_compliant_classes.append(class_name)
            elif line.startswith("def "):
                function_name = line.split()[1].split('(')[0]
                if not snake_case.match(function_name):
                    non_compliant_functions.append(function_name)
        
        self.report_data['Non-Compliant Classes'] = (
            non_compliant_classes if non_compliant_classes else ["All classes follow CamelCase"]
        )
        self.report_data['Non-Compliant Functions'] = (
            non_compliant_functions if non_compliant_functions else ["All functions follow snake_case"]
        )

    def generate_report(self):
        report_file = f"style_report_{self.file_path.split('/')[-1].replace('.py', '')}.txt"
        with open(report_file, 'w') as file:
            file.write("File Structure\n")
            file.write(f"Total lines: {self.report_data['Total Lines']}\n\n")
            
            file.write("Imports\n")
            for imp in self.report_data['Imports']:
                file.write(f"{imp}\n")
            file.write("\n")
            
            file.write("Classes\n")
            for cls in self.report_data['Classes']:
                file.write(f"{cls}\n")
            file.write("\n")
            
            file.write("Functions\n")
            for func in self.report_data['Functions']:
                file.write(f"{func}\n")
            file.write("\n")
            
            file.write("DocStrings\n")
            for doc in self.report_data['DocStrings']:
                file.write(f"{doc}\n\n")
            
            file.write("Type Annotation Check\n")
            for item in self.report_data['Missing Type Annotations']:
                file.write(f"{item}\n")
            file.write("\n")
            
            file.write("Naming Convention Check\n")
            file.write("Non-Compliant Classes\n")
            for cls in self.report_data['Non-Compliant Classes']:
                file.write(f"{cls}\n")
            file.write("Non-Compliant Functions\n")
            for func in self.report_data['Non-Compliant Functions']:
                file.write(f"{func}\n")

if __name__ == "__main__":
    checker = StyleChecker("sample.py")
    checker.read_file()
    checker.file_structure()
    checker.find_imports()
    checker.find_classes()
    checker.find_functions()
    checker.check_docstrings()
    checker.check_type_annotations()
    checker.check_naming_conventions()
    checker.generate_report()
    print("Style report generated successfully.")
