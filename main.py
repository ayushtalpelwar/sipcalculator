from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from enum import Enum
from typing import Dict

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class Frequency(str, Enum):
    monthly = "monthly"
    yearly = "yearly"

class SIPInput(BaseModel):
    investment: float = Field(..., gt=0, description="The amount to invest in each period (monthly or yearly)")
    annual_return_rate: float = Field(..., gt=0, le=100, description="The expected annual return rate as a percentage")
    investment_duration_years: int = Field(..., gt=0, description="The duration of the investment in years")
    frequency: Frequency

class LumpsumInput(BaseModel):
    initial_investment: float = Field(..., gt=0, description="The initial lumpsum investment amount")
    annual_return_rate: float = Field(..., gt=0, le=100, description="The expected annual return rate as a percentage")
    investment_duration_years: int = Field(..., gt=0, description="The duration of the investment in years")

class BreakdownResponse(BaseModel):
    total_invested: float
    final_profit: float
    profit_percentage: float
    maturity_amount: float

@app.post("/calculate_sip/", response_model=BreakdownResponse)
def calculate_sip(sip_input: SIPInput) -> BreakdownResponse:
    P = sip_input.investment
    
    if sip_input.frequency == Frequency.monthly:
        r = sip_input.annual_return_rate / 100 / 12
        n = sip_input.investment_duration_years * 12
    elif sip_input.frequency == Frequency.yearly:
        r = sip_input.annual_return_rate / 100
        n = sip_input.investment_duration_years

    future_value = P * (((1 + r) ** n - 1) / r) * (1 + r)
    total_invested = P * n
    final_profit = future_value - total_invested
    profit_percentage = (final_profit / total_invested) * 100
    
    return BreakdownResponse(
        maturity_amount=round(future_value, 2),
        total_invested=round(total_invested, 2),
        final_profit=round(final_profit, 2),
        profit_percentage=round(profit_percentage, 2)
    )

@app.post("/calculate_lumpsum/", response_model=BreakdownResponse)
def calculate_lumpsum(lumpsum_input: LumpsumInput) -> BreakdownResponse:
    P = lumpsum_input.initial_investment
    r = lumpsum_input.annual_return_rate / 100
    n = lumpsum_input.investment_duration_years

    future_value = P * (1 + r) ** n
    total_invested = P
    final_profit = future_value - total_invested
    profit_percentage = (final_profit / total_invested) * 100
    
    return BreakdownResponse(
        maturity_amount=round(future_value, 2),
        total_invested=round(total_invested, 2),
        final_profit=round(final_profit, 2),
        profit_percentage=round(profit_percentage, 2)
    )

# Route to serve the HTML page
@app.get("/")
def read_index():
    return {"message": "Visit /static/index.html to access the site"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)