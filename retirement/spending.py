from dataclasses import dataclass

@dataclass
class SpendingBreakdown:
    housing: float
    living: float
    travel: float
    healthcare: float
    charity: float
    one_time: float = 0.0

    @property
    def total(self) -> float:
        return (
            self.housing + self.living + self.travel +
            self.healthcare + self.charity + self.one_time
        )

class SpendingEngine:
    def spending_for_year(self, year:int)->SpendingBreakdown:
        years = year - 2026

        housing = 33600 * (1.03 ** years)
        living = 60000 * (1.025 ** years)

        base_travel = 120000 if years < 10 else 60000
        travel = base_travel * (1.03 ** years)

        healthcare = 23000 if year < 2029 else 10000
        healthcare *= (1.05 ** years)

        charity = 5000 * (1.025 ** years)

        one_time = 0
        if year == 2027:
            one_time += 20000
        if year == 2028:
            one_time += 50000

        return SpendingBreakdown(
            housing=housing,
            living=living,
            travel=travel,
            healthcare=healthcare,
            charity=charity,
            one_time=one_time,
        )
