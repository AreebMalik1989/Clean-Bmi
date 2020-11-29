import core
from core import Unit, Gender, Entry
from repository import Repository


class CliSupplier(core.BmiSupplier):

    def get_name(self) -> str:
        return input('name: ')

    def get_age(self) -> int:
        try:
            return int(input('age: '))
        except:
            return self.get_age()

    def get_gender(self) -> Gender:
        g = input('gender(m/f): ')
        return (
            Gender.MALE if g == 'm' else
            Gender.FEMALE if g == 'f' else
            self.get_gender()
        )

    def get_height(self) -> float:
        try:
            return float(input('height: '))
        except:
            return self.get_height()

    def get_height_unit(self) -> Unit.LengthUnit:
        u = input('height unit (m/cm/inch/foot-inch): ')
        return (
            Unit.LengthUnit.METER if u == 'm' else
            Unit.LengthUnit.CENTIMETER if u == 'cm' else
            Unit.LengthUnit.INCH if u == 'inch' else
            Unit.LengthUnit.FOOT_INCH if u == 'foot-inch' else
            self.get_height_unit()
        )

    def get_weight(self) -> float:
        try:
            return float(input('weight: '))
        except:
            return self.get_weight()

    def get_weight_unit(self) -> Unit.WeightUnit:
        u = input('weight unit (kg/lb/st): ')
        return (
            Unit.WeightUnit.KG if u == 'kg' else
            Unit.LengthUnit.CENTIMETER if u == 'lb' else
            Unit.LengthUnit.INCH if u == 'st' else
            self.get_weight_unit()
        )


if __name__ == "__main__":

    supplier = CliSupplier()
    repository = Repository()
    calculator = core.BmiCalculator(supplier, repository)
    a, b = calculator.calculate()
    print(f'bmi: {a}, category: {b}')

    calculator.save()
    print(*calculator.all_entries())
