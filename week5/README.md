# Week 5 – Token Economics: Cost and Rate-Limit Budgeting

## Aim

The aim of this task was to create a Python program that calculates the token usage and estimated cost of an AI application. I also worked on checking whether the application stays within the given daily budget, monthly budget and API rate limits.

## Technologies Used

- Python
- python-dotenv
- VS Code
- Environment Variables (.env)
- Unittest

## Project Files

- `budget.py` – Contains the code for calculating token usage, API costs and checking limits.
- `test_budget.py` – Used to test whether the calculations are working correctly.
- `requirements.txt` – Contains the required Python package.
- `.env` – Stores the token usage, pricing and budget details.
- `.env.example` – Contains an example of the configuration values.

## Execution

First, I installed the required package using the following command:

```bash
python -m pip install -r week5/requirements.txt
```

After installing the package, I ran the budget planner using:

```bash
python week5/budget.py
```

The program used the values stored in the `.env` file, such as daily requests, input tokens, output tokens, API pricing and budget limits.

It calculated the daily input tokens, output tokens, total token usage, estimated daily cost and monthly cost.

It also checked the RPM (Requests Per Minute) and TPM (Tokens Per Minute) limits and displayed whether each condition passed or failed.

I then executed the unit tests using:

```bash
python -m unittest week5/test_budget.py -v
```

All four unit tests passed successfully.

## What I Understood

Through this task, I understood how token usage affects the cost of an AI application. I learned that both input tokens and output tokens are considered when calculating the API cost.

I also understood the meaning of RPM and TPM and why it is important to check these limits before using an AI application.

Another thing I learned was how to use environment variables to store values separately from the Python code. This makes it easier to change the pricing and budget details whenever required.

I also performed a What-If Analysis by increasing the daily requests from 2000 to 4000. I observed that the token usage and estimated cost also doubled, causing the daily and monthly budget checks to fail.

## Result

Successfully implemented and executed the Token Economics Budget Planner. The program calculated the token usage and estimated API costs, checked the budget and rate limits, and displayed a GO or NO-GO recommendation.

All four unit tests passed successfully. The initial configuration passed all the budget and rate-limit checks.

## Conclusion

This task helped me understand how to estimate and manage the cost of using AI models. I also learned about token consumption, API pricing, rate limits and unit testing. By performing the What-If Analysis, I understood how increasing the number of requests can affect the overall cost of an AI application.