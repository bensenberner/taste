from taste_analysis import TasteAnalysis


class TestTasteAnalysis:
    TINY_CSV_PATH = "test_tiny_customers.csv"

    def run_tests(self):
        if (
            self.test_tiny_init()
            and self.test_tiny_best_customers()
            and self.test_tiny_customer_repeat_rate()
            and self.test_tiny_weekly_cohort_analysis()
        ):
            print("\n\n=====CONGRATULATIONS! ALL TESTS PASSED!=====\n\n")
        else:
            print("\n\n*****SOME TESTS FAILED*****\n\n")

    def test_tiny_init(self) -> bool:
        try:
            analyzer = TasteAnalysis(TestTasteAnalysis.TINY_CSV_PATH)
            assert analyzer.row_count == 38
            """
            Fill in the correct test cases here
            assert analyzer.customers == None
            assert analyzer.freq_count == None
            """
            print("PASSED: test_tiny_init")
            return True
        except AssertionError:
            print("*****FAILED*****: test_tiny_init")
            return False

    def test_tiny_best_customers(self) -> bool:
        try:
            analyzer = TasteAnalysis(TestTasteAnalysis.TINY_CSV_PATH)
            best_customers = analyzer.print_best_customers()
            assert len(best_customers) == 1
            assert best_customers[0][0] == 4
            assert best_customers[0][1] == "jcagmn2k01@agoagmail.com"
            print("PASSED: test_tiny_best_customers")
            return True
        except AssertionError:
            print("*****FAILED*****: test_tiny_best_customers")
            return False

    def test_tiny_customer_repeat_rate(self) -> bool:
        try:
            analyzer = TasteAnalysis(TestTasteAnalysis.TINY_CSV_PATH)
            customer_repeat_rate = analyzer.print_customer_repeat_rate()
            assert len(customer_repeat_rate) == 4
            assert customer_repeat_rate[0][1] == 38
            assert customer_repeat_rate[1][1] == 35
            assert customer_repeat_rate[2][0] == "1 Count"
            assert customer_repeat_rate[3][0] == "4 Count"
            assert customer_repeat_rate[2][1] == 34
            assert customer_repeat_rate[3][1] == 1

            print("PASSED: test_tiny_customer_repeat_rate")
            return True
        except AssertionError:
            print("*****FAILED*****: test_tiny_customer_repeat_rate")
            return False

    def test_tiny_weekly_cohort_analysis(self) -> bool:
        try:
            analyzer = TasteAnalysis(TestTasteAnalysis.TINY_CSV_PATH)
            weekly_cohort_analysis = analyzer.print_weekly_cohort_analysis()
            assert len(weekly_cohort_analysis) == 15

            assert weekly_cohort_analysis[1][0] == "2020-04-18"
            assert str(weekly_cohort_analysis[1][1]) == "35"
            assert weekly_cohort_analysis[1][2] == "0 (0%)"
            assert weekly_cohort_analysis[1][3] == "35 (100%)"
            assert str(weekly_cohort_analysis[1][4]) == "1.09"
            print("PASSED: test_tiny_weekly_cohort_analysis")
            return True
        except AssertionError:
            print("*****FAILED*****: test_tiny_weekly_cohort_analysis")
            return False

    """
    Write your other tests in this section
    """


tta = TestTasteAnalysis()
tta.run_tests()
