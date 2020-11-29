import dataclasses
import sqlite3
import core


class Repository(core.BmiRepository):

    def __init__(self):
        self._connect()
        self._c.execute("""
        CREATE TABLE IF NOT EXISTS entries(
        name text,
        age integer,
        gender text,
        bmi real,
        bmiCategory text,
        timestamp real)
        """)

    def save(self, entry: core.Entry) -> bool:
        data_entry = DataEntry.from_entry(entry)
        try:
            self._connect()
            self._c.execute("""
                    INSERT INTO entries VALUES
                    (?, ?, ?, ?, ?, ?)""",
                            (data_entry.name,
                             data_entry.age,
                             data_entry.gender,
                             data_entry.bmi,
                             data_entry.bmi_category,
                             data_entry.timestamp)
                            )
            self._commit()
        except:
            return False
        finally:
            self._close()

        return True

    def all(self) -> tuple[core.Entry]:
        try:
            self._connect()
            self._c.execute('SELECT * FROM entries')
            entries = list()
            for e in self._c.fetchall():
                entries.append(DataEntry(*e).to_entry())

        finally:
            self._close()

        return tuple(entries)

    def _connect(self):
        self._conn = sqlite3.connect('repository.db')
        self._c = self._conn.cursor()

    def _commit(self):
        self._conn.commit()

    def _close(self):
        self._conn.close()


@dataclasses.dataclass(frozen=True)
class DataEntry:
    name: str
    age: int
    gender: str
    bmi: float
    bmi_category: str
    timestamp: float

    def to_entry(self) -> core.Entry: return core.Entry(
        self.name,
        self.age,
        core.Gender.parse(self.gender),
        self.bmi,
        core.BmiCategory.parse(self.bmi_category),
        self.timestamp
    )

    @staticmethod
    def from_entry(entry: core.Entry): return DataEntry(
        entry.name,
        entry.years_age,
        entry.gender.value,
        entry.bmi,
        entry.bmi_category.value,
        entry.timestamp
    )
