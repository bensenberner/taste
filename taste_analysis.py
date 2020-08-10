import sys
from collections import Counter
from datetime import timedelta
from typing import Any, List, Tuple, NamedTuple

import pandas as pd
from dateutil import parser
from tabulate import tabulate


class CustomerCount(NamedTuple):
    count: int
    email: str


class AnalysisException(Exception):
    pass


class TasteAnalysis:
    LAST_COHORT_END = parser.parse("2020-07-25 00:00 UTC")  # Saturday
    FIRST_COHORT_START = parser.parse("2020-04-18 00:00 UTC")
    MAX_NUM_COHORTS = (LAST_COHORT_END - FIRST_COHORT_START).days // 7
    BEST_CUSTOMER_MIN = 2  # Min is 2 orders

    class CohortAnalysis:
        """
        Using a nested class to take advantage of TasteAnalysis class vars
        """

        WEEK_LATER = timedelta(weeks=1)

        def __init__(self):
            self.results = []
            self.total_num_purchases = 0
            self.curr_cohort_start = TasteAnalysis.FIRST_COHORT_START
            self.curr_cohort_customers = set()
            self.all_customers = set()
            self.curr_cohort_repeat_customer_count = 0
            self.curr_cohort_new_customer_count = 0

        def fill_rest_of_results(self):
            while len(self.results) < TasteAnalysis.MAX_NUM_COHORTS:
                self._add_to_results_and_refresh_local_data()

        def _refresh_cohort_data_for_new_cohort(self):
            self.curr_cohort_start += self.WEEK_LATER
            self.curr_cohort_customers = set()
            self.curr_cohort_new_customer_count = 0
            self.curr_cohort_repeat_customer_count = 0

        def _add_to_results_and_refresh_local_data(self):
            if self.total_num_purchases == 0:
                raise ZeroDivisionError(
                    "Need at least one transaction in the whole dataset"
                )
            total_cohort_customers = len(self.curr_cohort_customers)
            cohort_repeat_percent = (
                (100 * self.curr_cohort_repeat_customer_count / total_cohort_customers)
                if total_cohort_customers
                else 0
            )
            cohort_new_percent = (
                (100 * self.curr_cohort_new_customer_count / total_cohort_customers)
                if total_cohort_customers
                else 0
            )
            avg_purchases_since_beginning = self.total_num_purchases / len(
                self.all_customers
            )
            new_result = [
                self.curr_cohort_start.strftime("%Y-%m-%d"),
                total_cohort_customers,
                f"{self.curr_cohort_repeat_customer_count} ({cohort_repeat_percent:.0f}%)",
                f"{self.curr_cohort_new_customer_count} ({cohort_new_percent:.0f}%)",
                f"{avg_purchases_since_beginning:.2f}",
            ]
            self.results.append(new_result)
            self._refresh_cohort_data_for_new_cohort()

        def process_transaction(self, email, date):
            if len(self.results) == TasteAnalysis.MAX_NUM_COHORTS:
                raise AnalysisException(
                    f"Cannot have more than {TasteAnalysis.MAX_NUM_COHORTS} cohorts"
                )
            if date > TasteAnalysis.LAST_COHORT_END:
                raise AnalysisException(
                    f"Cannot add data past {TasteAnalysis.LAST_COHORT_END}"
                )
            self.total_num_purchases += 1
            if date > self.curr_cohort_start + self.WEEK_LATER:
                self._add_to_results_and_refresh_local_data()
            if email in self.all_customers:
                if email not in self.curr_cohort_customers:
                    self.curr_cohort_repeat_customer_count += 1
            else:
                self.curr_cohort_new_customer_count += 1
            self.all_customers.add(email)
            self.curr_cohort_customers.add(email)

    @property
    def customers(self):
        return self.freq_counts.keys()

    def __init__(self, path: str) -> None:
        print(f"Processing csv at: {path}")
        self.data: pd.DataFrame = pd.read_csv(path, parse_dates=True, header=0)
        self.data.reindex(index=self.data.index[::-1])
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
        print("=====WEEKLY COHORT ANALYSIS=====")
        table = [
            [
                "Cohort Start Date",
                "Total Cohort Customers",
                "Repeat Customers (%)",
                "New Customers (%)",
                "Buy Avg",
            ]
        ]
        cohort_analysis = self.CohortAnalysis()
        for _, row in self.data.iterrows():
            email, date = row["Email"], row["Created (UTC)"]
            cohort_analysis.process_transaction(email, date)
        cohort_analysis.fill_rest_of_results()
        table += cohort_analysis.results
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
