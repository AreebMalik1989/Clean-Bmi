import abc
import enum
import dataclasses
import time


class BmiCategory(enum.Enum):
    VERY_SEVERELY_UNDERWEIGHT = "Very Severely Underweight"
    SEVERELY_UNDERWEIGHT = "Severely Underweight"
    UNDERWEIGHT = "Underweight"
    NORMAL = "Normal Weight"
    OVER_WEIGHT = "Overweight"
    OBESE_I = "Class-I Obese"
    OBESE_II = "Class-II Obese"
    OBESE_III = "Class-III Obese"
    UNKNOWN = "Unknown"

    @classmethod
    def parse(cls, bmi_category: str): return (

        cls.VERY_SEVERELY_UNDERWEIGHT
        if bmi_category == cls.VERY_SEVERELY_UNDERWEIGHT.value else

        cls.SEVERELY_UNDERWEIGHT
        if bmi_category == cls.SEVERELY_UNDERWEIGHT.value else

        cls.UNDERWEIGHT
        if bmi_category == cls.UNDERWEIGHT.value else

        cls.NORMAL
        if bmi_category == cls.NORMAL.value else

        cls.OVER_WEIGHT
        if bmi_category == cls.OVER_WEIGHT.value else

        cls.OBESE_I
        if bmi_category == cls.OBESE_I.value else

        cls.OBESE_II
        if bmi_category == cls.OBESE_II.value else

        cls.OBESE_III
        if bmi_category == cls.OBESE_III.value else

        cls.UNKNOWN
    )


class Gender(enum.Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def parse(cls, gender: str): return (
        cls.MALE if gender == cls.MALE.value else
        cls.FEMALE if gender == cls.FEMALE.value else
        cls.UNKNOWN
    )


class Unit:
    class WeightUnit(enum.Enum):
        KG = 'Kilogram'
        POUND = "Pound"
        STONE_POUND = "Stone-Pound"
        UNKNOWN = "Unknown"

        @classmethod
        def parse(cls, unit: str): return (
            cls.KG if unit == cls.KG.value else
            cls.POUND if unit == cls.POUND.value else
            cls.STONE_POUND if unit == cls.STONE_POUND.value else
            cls.UNKNOWN
        )

    class LengthUnit(enum.Enum):
        METER = "Meter"
        CENTIMETER = "Centimeter"
        FOOT_INCH = "Foot-Inch"
        INCH = "Inch"
        UNKNOWN = "Unknown"

        @classmethod
        def parse(cls, unit: str): return (
            cls.METER if unit == cls.METER.value else
            cls.CENTIMETER if unit == cls.CENTIMETER.value else
            cls.FOOT_INCH if unit == cls.FOOT_INCH.value else
            cls.INCH if unit == cls.INCH.value else
            cls.UNKNOWN
        )


@dataclasses.dataclass(frozen=True)
class Entry:
    name: str
    years_age: int
    gender: Gender
    bmi: float
    bmi_category: BmiCategory
    timestamp: float


@dataclasses.dataclass(frozen=True)
class Height:
    height: float
    unit: Unit.LengthUnit


@dataclasses.dataclass(frozen=True)
class Weight:
    weight: float
    unit: Unit.WeightUnit


def _convert_height(h: Height) -> float: return (
    h.height if h.unit == Unit.LengthUnit.METER else
    h.height * 0.0254 if h.unit == Unit.LengthUnit.INCH else
    h.height * 0.01 if h.unit == Unit.LengthUnit.CENTIMETER else
    -1
)


def _convert_weight(w: Weight) -> float: return (
    w.weight if w.unit == Unit.WeightUnit.KG else
    w.weight * 0.453592 if w.unit == Unit.WeightUnit.POUND else
    w.weight * 0.157473 if w.unit == Unit.WeightUnit.STONE_POUND else
    -1
)


def _calculate_bmi(meter_height: float, kg_weight: float) -> float:
    return (
        -1.0 if meter_height <= 0 or kg_weight <= 0 else
        ((kg_weight/meter_height)/meter_height)
    )


def _translate_bmi(bmi: float) -> BmiCategory: return (
    BmiCategory.VERY_SEVERELY_UNDERWEIGHT if bmi < 16 else
    BmiCategory.SEVERELY_UNDERWEIGHT if bmi < 17 else
    BmiCategory.UNDERWEIGHT if bmi < 18.5 else
    BmiCategory.NORMAL if bmi < 25 else
    BmiCategory.OVER_WEIGHT if bmi < 30 else
    BmiCategory.OBESE_I if bmi < 35 else
    BmiCategory.OBESE_II if bmi < 40 else
    BmiCategory.OBESE_III if bmi >= 40 else
    BmiCategory.UNKNOWN
)


class BmiSupplier(abc.ABC):

    @abc.abstractmethod
    def get_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_age(self) -> int:
        pass

    @abc.abstractmethod
    def get_gender(self) -> Gender:
        pass

    @abc.abstractmethod
    def get_height(self) -> float:
        pass

    @abc.abstractmethod
    def get_height_unit(self) -> Unit.LengthUnit:
        pass

    @abc.abstractmethod
    def get_weight(self) -> float:
        pass

    @abc.abstractmethod
    def get_weight_unit(self) -> Unit.WeightUnit:
        pass


class BmiRepository(abc.ABC):

    @abc.abstractmethod
    def save(self, entry: Entry) -> bool:
        pass

    @abc.abstractmethod
    def all(self) -> tuple[Entry]:
        pass


@dataclasses.dataclass(frozen=True)
class BmiCalculator:
    supplier: BmiSupplier
    repository: BmiRepository

    def calculate(self) -> tuple[float, BmiCategory]:
        h = self.supplier.get_height()
        hu = self.supplier.get_height_unit()
        w = self.supplier.get_weight()
        wu = self.supplier.get_weight_unit()
        height: float = _convert_height(Height(h, hu))
        weight: float = _convert_weight(Weight(w, wu))
        bmi = _calculate_bmi(height, weight)
        return bmi, _translate_bmi(bmi)

    def save(self) -> bool:
        name = self.supplier.get_name()
        age = self.supplier.get_age()
        gender = self.supplier.get_gender()
        e = Entry(name, age, gender, *self.calculate(), time.time())

        return self.repository.save(e)

    def all_entries(self) -> tuple[Entry]:
        return self.repository.all()
