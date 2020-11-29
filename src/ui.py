import tkinter
from tkinter import ttk
import core
from core import Unit, Gender
from repository import Repository


class Application(tkinter.Frame, core.BmiSupplier):

    repository = Repository()

    NAME = 'Name'
    AGE = 'Age'
    GENDER = 'Gender'
    HEIGHT = 'Height'
    WEIGHT = 'Weight'
    CALCULATE = 'Calculate'
    RESULT = 'Result'
    SHOW_ALL = 'Show All Results'
    BMI = 'BMI'
    BMI_CATEGORY = 'BMI Category'
    TIMESTAMP = 'Timestamp'

    def __init__(self, master=None):
        super().__init__(master=master)
        self.name_label = ttk.Label(master=master, text=self.NAME)
        self.name = ttk.Entry(master=master)
        self.age_label = ttk.Label(master=master, text=self.AGE)
        self.age = ttk.Entry(master=master)
        self.gender_label = ttk.Label(master=master, text=self.GENDER)
        self.gender = ttk.Combobox(master=master)
        self.gender['values'] = (core.Gender.MALE.value,
                                 core.Gender.FEMALE.value)
        self.height_label = ttk.Label(master=master, text=self.HEIGHT)
        self.height = ttk.Entry(master=master)
        self.height_unit = ttk.Combobox(master=master)
        self.height_unit['values'] = (core.Unit.LengthUnit.METER.value,
                                      core.Unit.LengthUnit.CENTIMETER.value,
                                      core.Unit.LengthUnit.INCH.value,
                                      core.Unit.LengthUnit.FOOT_INCH.value)
        self.weight_label = ttk.Label(master=master, text=self.WEIGHT)
        self.weight = ttk.Entry(master=master)
        self.weight_unit = ttk.Combobox(master=master)
        self.weight_unit['values'] = (core.Unit.WeightUnit.KG.value,
                                      core.Unit.WeightUnit.POUND.value,
                                      core.Unit.WeightUnit.STONE_POUND.value)
        self.calculate = ttk.Button(master=master, text=self.CALCULATE, command=self.calculate_result)
        self.show_all = ttk.Button(master=master, text=self.SHOW_ALL, command=self.show_all_results)
        self.result_label = ttk.Label(master=master, text=self.RESULT)
        self.result_bmi = ttk.Label(master=master)
        self.result_bmi_category = ttk.Label(master=master)

        self.name_label.grid(row=0, column=0, columnspan=1, sticky='NSEW')
        self.name.grid(row=0, column=1, columnspan=2, sticky='NSEW')
        self.age_label.grid(row=1, column=0, columnspan=1, sticky='NSEW')
        self.age.grid(row=1, column=1, columnspan=2, sticky='NSEW')
        self.gender_label.grid(row=2, column=0, columnspan=1, sticky='NSEW')
        self.gender.grid(row=2, column=1, columnspan=2, sticky='NSEW')
        self.height_label.grid(row=3, column=0, columnspan=1, sticky='NSEW')
        self.height.grid(row=3, column=1, columnspan=1, sticky='NSEW')
        self.height_unit.grid(row=3, column=2, columnspan=1, sticky='NSEW')
        self.weight_label.grid(row=4, column=0, columnspan=1, sticky='NSEW')
        self.weight.grid(row=4, column=1, columnspan=1, sticky='NSEW')
        self.weight_unit.grid(row=4, column=2, columnspan=1, sticky='NSEW')
        self.calculate.grid(row=5, column=0, columnspan=3, sticky='NSEW')
        self.show_all.grid(row=6, column=0, columnspan=3, sticky='NSEW')
        self.result_label.grid(row=7, column=0, columnspan=1, sticky='NSEW')
        self.result_bmi.grid(row=7, column=1, columnspan=1, sticky='NSEW')
        self.result_bmi_category.grid(row=7, column=2, columnspan=1, sticky='NSEW')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=3)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)

    def get_name(self) -> str:
        return self.name.get()

    def get_age(self) -> int:
        return self.age.get()

    def get_gender(self) -> Gender:
        return Gender.parse(self.gender.get())

    def get_height(self) -> float:
        return float(self.height.get())

    def get_height_unit(self) -> Unit.LengthUnit:
        return core.Unit.LengthUnit.parse(self.height_unit.get())

    def get_weight(self) -> float:
        return float(self.weight.get())

    def get_weight_unit(self) -> Unit.WeightUnit:
        return core.Unit.WeightUnit.parse(self.weight_unit.get())

    def calculate_result(self):
        calculator = core.BmiCalculator(self, self.repository)
        a, b = calculator.calculate()
        calculator.save()
        self.result_bmi['text'] = str(a)
        self.result_bmi_category['text'] = b.value

    def show_all_results(self):
        new_window = tkinter.Toplevel(self)
        new_window.title('Results')

        values = self.repository.all()

        for i in range(len(values)):
            label = ttk.Label(master=new_window, text=values[i])
            label.pack()


root = tkinter.Tk()
root.title('BMI Calculator')
app = Application(master=root)
app.mainloop()
