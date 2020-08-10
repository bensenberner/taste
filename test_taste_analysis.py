from unittest import TestCase

from taste_analysis import TasteAnalysis


class TestTasteAnalysis(TestCase):
    TINY_CSV_PATH = "test_tiny_customers.csv"

    def test_tiny_init(self):
        analyzer = TasteAnalysis(TestTasteAnalysis.TINY_CSV_PATH)
        self.assertEqual(38, analyzer.row_count)
        self.assertEqual(35, len(analyzer.customers))
        """
        Fill in the correct test cases here
        assert analyzer.customers == None
        assert analyzer.freq_count == None
        """

    def test_tiny_best_customers(self):
        analyzer = TasteAnalysis(TestTasteAnalysis.TINY_CSV_PATH)
        best_customers = analyzer.print_best_customers()
        self.assertEqual(1, len(best_customers))
        self.assertEqual(4, best_customers[0][0])
        self.assertEqual("jcagmn2k01@agoagmail.com", best_customers[0][1])

    def test_tiny_customer_repeat_rate(self):
        analyzer = TasteAnalysis(TestTasteAnalysis.TINY_CSV_PATH)
        customer_repeat_rate = analyzer.print_customer_repeat_rate()
        self.assertEqual(4, len(customer_repeat_rate))
        self.assertEqual(38, customer_repeat_rate[0][1])
        self.assertEqual(35, customer_repeat_rate[1][1])
        self.assertEqual("1 Count", customer_repeat_rate[2][0])
        self.assertEqual("4 Count", customer_repeat_rate[3][0])
        self.assertEqual(34, customer_repeat_rate[2][1])
        self.assertEqual(1, customer_repeat_rate[3][1])

    def test_tiny_weekly_cohort_analysis(self):
        analyzer = TasteAnalysis(TestTasteAnalysis.TINY_CSV_PATH)
        weekly_cohort_analysis = analyzer.print_weekly_cohort_analysis()
        self.assertEqual(15, len(weekly_cohort_analysis))
        self.assertEqual("2020-04-18", weekly_cohort_analysis[1][0])
        self.assertEqual("35", str(weekly_cohort_analysis[1][1]))
        self.assertEqual("0 (0%)", weekly_cohort_analysis[1][2])
        self.assertEqual("35 (100%)", weekly_cohort_analysis[1][3])
        self.assertEqual("1.09", str(weekly_cohort_analysis[1][4]))
