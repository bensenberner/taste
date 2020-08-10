import sys
from collections import Counter
from datetime import timedelta
from typing import Any, List, Tuple, NamedTuple

import pandas as pd
from dateutil import parser
from pytz import utc
from tabulate import tabulate


class CustomerCount(NamedTuple):
    count: int
    email: str


class TasteAnalysis:
    LAST_COHORT_END = parser.parse("2020-07-25 00:00 UTC")  # Saturday
    FIRST_COHORT_START = parser.parse("2020-04-18 00:00 UTC")
    BEST_CUSTOMER_MIN = 2  # Min is 2 orders

    """
    Reads in the CSV file and sets member variables as needed
    """

    @property
    def customers(self):
        return self.freq_counts.keys()

    def __init__(self, path: str) -> None:
        print(f"Processing csv at: {path}")
        self.data: pd.DataFrame = pd.read_csv(path, parse_dates=True, header=0).iloc[
            ::-1
        ]
        self.data["Created (UTC)"] = pd.to_datetime(
            self.data["Created (UTC)"], utc=True
        )
        self.row_count = self.data.shape[0]
        self.freq_counts = self.data["Email"].value_counts()
        self.best_customers: List[Tuple[int, str]] = [
            (count, email)
            for email, count in self.freq_counts[
                self.freq_counts > self.BEST_CUSTOMER_MIN
            ].iteritems()
        ]
        """
        Hint: create a class member data structure to store self.customers, 
              optionally create a data structure to store frequency count
        """

        print("Finished processing: ", self.row_count)
        print("\n\n")

    def gen_reports(self) -> None:
        self.print_best_customers()
        self.print_customer_repeat_rate()
        self.print_weekly_cohort_analysis()

    """
    Prints the best customers. One per line. A 'Best Customer' is
    where the purchase count is greater than or equal to 
    TasteAnalysis.BEST_CUSTOMER_MIN.

    Returns a List of Tuples. Each tuple is a the number of purchases
    made by Best Customer and the customer email.
    """

    def print_best_customers(self) -> List[Tuple[int, str]]:
        print("=====BEST CUSTOMERS=====")
        for element in self.best_customers:
            print(element)
        print("\n\n")
        return self.best_customers

    """
    Prints the customer repeat rate
    Total Purchases Count       [Count]
    Unique Customers            [Count]
    1 Count                     [Count]
    ... (continues with 2,3,4,5... if they exist)

    Returns the argument to tabulate: type List[List[Any]]
    """

    def print_customer_repeat_rate(self) -> List[List[Any]]:
        print("=====CUSTOMER REPEAT RATE=====")
        table: List[List[Any]] = [
            ["Total Purchases Count", self.row_count],
            ["Unique Customers", len(self.freq_counts.keys())],
        ] + [
            [f"{count} Count", count_of_counts]
            for count, count_of_counts in Counter(
                sorted(self.freq_counts.tolist())
            ).items()
        ]
        print(tabulate(table))
        print("\n\n")
        return table

    """
    Each row has a Cohort Start Date, which are weekly dates starting from 4/18
    
    Total Cohort Customers: are all the unique customers who purchased during that week
    
    Repeat Customers (%): is the number of customers in that week who have purchased 
    in previous weeks. 
    Percent is shown in parenthesis - 100 * Repeat Customers / Total Cohort Customers.

    New Customers (%): is the number of customers who are new that week. 
    Percent is shown in parenthesis - New Customers / Total Cohort Customers.

    Buy Avg: Total Orders made by new customers / New Customers. 
    Where Total Orders extends the entire duration of the data. 
    For example, if 5 customers bought once per week for 8 weeks, 
    then Total Orders is 40 and the Buy Avg = 40/5 = 8.

    Returns the table that tabulate prints
    """

    def print_weekly_cohort_analysis(self) -> List[List[Any]]:
        # calculate repeat purchases by cohort
        print("=====WEEKLY COHORT ANALYSIS=====")

        table = []
        table.append(
            [
                "Cohort Start Date",
                "Total Cohort Customers",
                "Repeat Customers (%)",
                "New Customers (%)",
                "Buy Avg",
            ]
        )
        curr_cohort_start = self.data["Created (UTC)"].iloc[0]
        customers_seen = set()
        results = []
        curr_cohort_new_customers = 0
        curr_cohort_repeat_customers = 0
        week_later = timedelta(weeks=1)

        for _, row in self.data.iterrows():
            email, date = row["Email"], row["Created (UTC)"]
            if date > self.LAST_COHORT_END:
                break
            if date > curr_cohort_start + week_later:
                total_cohort_customers = (
                    curr_cohort_new_customers + curr_cohort_repeat_customers
                )
                results.append(
                    [
                        curr_cohort_start,
                        total_cohort_customers,
                        curr_cohort_repeat_customers / total_cohort_customers,
                        curr_cohort_new_customers / total_cohort_customers,
                        0,  # TODO: what does average mean?
                    ]
                )
                curr_cohort_start += week_later
                curr_cohort_new_customers = 0
                curr_cohort_repeat_customers = 0
            if email in customers_seen:
                curr_cohort_repeat_customers += 1
            else:
                curr_cohort_new_customers += 1
            customers_seen.add(email)

        while curr_cohort_start < self.LAST_COHORT_END:
            curr_cohort_start += week_later
        print(tabulate(table, headers="firstrow"))
        return table


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please enter a valid csv file path")
    else:
        csv_path = sys.argv[1]
        assert csv_path is not None

        analyzer = TasteAnalysis(csv_path)
        analyzer.gen_reports()
