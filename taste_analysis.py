import csv
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from tabulate import tabulate
from dateutil.tz import gettz
from dateutil.parser import parse
from typing import Dict, Any, List, Tuple
import sys


class TasteAnalysis:
    LAST_COHORT_END = "2020-07-25 00:00 UTC"  # Saturday
    FIRST_COHORT_START = "2020-04-18 00:00 UTC"
    BEST_CUSTOMER_MIN = 2  # Min is 2 orders

    """
    Reads in the CSV file and sets member variables as needed
    """

    def __init__(self, path: str) -> None:
        print(f"Processing csv at: {path}")
        self.row_count = 0

        """
       
        YOUR CODE HERE
        Process CSV and store in appropriate data structures
        
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
        best_customers: List[Tuple[int, str]] = []

        """
      
        YOUR CODE HERE

        """

        print("\n\n")

        return best_customers

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
        table: List[List[Any]] = []

        """
        
        YOUR CODE HERE
        
        """

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

        """
        
        YOUR CODE HERE

        """

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
