import pytest

from finance import (
	calculate_compound_interest,
	calculate_annuity_payment,
	calculate_internal_rate_of_return,
)


class TestCompoundInterest:
	@pytest.fixture(scope="class")
	def compound_data(self):
		return {
			"principal_default": 100.0,
			"rate_default": 0.05,
			"periods_default": 2,
			"principal_negative": -100.0,
			"rate_negative": -0.01,
			"periods_zero": 0,
		}

	@pytest.fixture(autouse=True)
	def _inject_compound(self, compound_data):
		self.data = compound_data

	def test_basic_compound_interest(self):
		expected = self.data["principal_default"] * ((1 + self.data["rate_default"]) ** self.data["periods_default"])
		assert calculate_compound_interest(self.data["principal_default"], self.data["rate_default"], self.data["periods_default"]) == pytest.approx(expected)

	def test_zero_rate_returns_principal(self):
		assert calculate_compound_interest(200.0, 0.0, 5) == pytest.approx(200.0)

	def test_zero_periods_returns_principal(self):
		assert calculate_compound_interest(50.0, 0.1, self.data["periods_zero"]) == pytest.approx(50.0)

	def test_negative_rate_reduces_value(self):
		expected = self.data["principal_default"] * ((1 + self.data["rate_negative"]) ** 3)
		assert calculate_compound_interest(self.data["principal_default"], self.data["rate_negative"], 3) == pytest.approx(expected)

	def test_negative_principal(self):
		expected = self.data["principal_negative"] * ((1 + self.data["rate_default"]) ** self.data["periods_default"])
		assert calculate_compound_interest(self.data["principal_negative"], self.data["rate_default"], self.data["periods_default"]) == pytest.approx(expected)


class TestAnnuityPayment:
	@pytest.fixture(scope="class")
	def annuity_data(self):
		return {
			"principal": 1000.0,
			"rate": 0.05,
			"periods": 10,
		}

	@pytest.fixture(autouse=True)
	def _inject_annuity(self, annuity_data):
		self.ad = annuity_data

	def test_annuity_zero_rate(self):
		expected = 1000.0 / 10
		assert calculate_annuity_payment(self.ad["principal"], 0.0, self.ad["periods"]) == pytest.approx(expected)

	def test_annuity_nonzero_rate(self):
		expected = self.ad["principal"] * (self.ad["rate"] * (1 + self.ad["rate"]) ** self.ad["periods"]) / ((1 + self.ad["rate"]) ** self.ad["periods"] - 1)
		assert calculate_annuity_payment(self.ad["principal"], self.ad["rate"], self.ad["periods"]) == pytest.approx(expected)

	def test_annuity_zero_periods_raises(self):
		with pytest.raises(ZeroDivisionError):
			calculate_annuity_payment(self.ad["principal"], 0.0, 0)

	def test_annuity_string_periods_type_error(self):
		with pytest.raises(TypeError):
			calculate_annuity_payment(self.ad["principal"], self.ad["rate"], "10")

	def test_annuity_negative_periods_with_zero_rate(self):
		assert calculate_annuity_payment(self.ad["principal"], 0.0, -10) == pytest.approx(self.ad["principal"] / -10)


class TestInternalRateOfReturn:
	@pytest.fixture(scope="class")
	def irr_data(self):
		return {
			"cf_two_period": [-100.0, 110.0],
			"cf_three_period": [-100.0, 60.0, 60.0],
			"cf_zeros": [0.0, 0.0, 0.0],
			"cf_single": [-100.0],
		}

	@pytest.fixture(autouse=True)
	def _inject_irr(self, irr_data):
		self.irr = irr_data

	def test_irr_two_period_exact(self):
		irr = calculate_internal_rate_of_return(self.irr["cf_two_period"], iterations=100)
		assert irr == pytest.approx(0.1, rel=1e-6)

	def test_irr_simple_approx(self):
		irr = calculate_internal_rate_of_return(self.irr["cf_three_period"], iterations=200)
		npv = sum(cf / (1 + irr) ** i for i, cf in enumerate(self.irr["cf_three_period"]))
		assert npv == pytest.approx(0.0, abs=1e-6)

	def test_irr_all_zeros_returns_initial_guess(self):
		irr = calculate_internal_rate_of_return(self.irr["cf_zeros"], iterations=10)
		assert irr == pytest.approx(0.1)

	def test_irr_none_raises_type_error(self):
		with pytest.raises(TypeError):
			calculate_internal_rate_of_return(None)

	def test_irr_single_cashflow_returns_guess(self):
		irr = calculate_internal_rate_of_return(self.irr["cf_single"], iterations=10)
		assert irr == pytest.approx(0.1)
