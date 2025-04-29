import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class BikeRepairShopSimulation:
    def __init__(self):
        # Time parameters
        self.days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        # Shop parameters
        self.mechanic_salary_per_day = 130  # € per day
        self.repair_price_average = 80  # € per repair
        self.parts_cost_average = 30  # € per repair
        self.max_queue_size = 30  # maximum bikes in queue

        # Seasonal base parameters - repairs per day by month
        self.monthly_base_repairs = [5, 8, 15, 25, 30, 35, 32, 30, 25, 15, 8, 10]

        # Weather impact parameters - independent from seasonality
        self.monthly_avg_precipitation = [70, 50, 60, 50, 60, 65, 70, 70, 60, 65, 80, 80]  # mm
        self.precipitation_impact_factor = -0.05  # % change per mm

        # Repair parameters
        self.repair_time_mean = 3.0  # hours
        self.repair_time_std = 1.0  # hours
        self.working_hours_per_day = 8  # hours

        # Parts requirements
        self.parts_probabilities = {
            "basic": 0.50,  # basic service
            "medium": 0.30, # medium parts cost
            "major": 0.20   # major parts cost
        }
        self.parts_costs = {
            "basic": 15,
            "medium": 50,
            "major": 120
        }

        # Customer satisfaction parameters
        self.max_acceptable_wait_days = 7
        self.satisfaction_decay_per_day = 0.15

    def generate_daily_repair_requests(self, month, precipitation):
        # Base request rate for this month
        base_requests = self.monthly_base_repairs[month]

        # Weather effect (independent from seasonality)
        avg_daily_precip = self.monthly_avg_precipitation[month] / self.days_in_month[month]
        precip_delta = precipitation - avg_daily_precip
        weather_factor = 1.0 + (precip_delta * self.precipitation_impact_factor)

        # Calculate expected requests and add randomness
        expected_requests = base_requests * weather_factor
        actual_requests = np.random.poisson(expected_requests)

        return max(0, actual_requests)

    def generate_repair_time(self):
        # Generate repair time (min 1 hour)
        repair_time = np.random.normal(self.repair_time_mean, self.repair_time_std)
        return max(1.0, repair_time)

    def determine_parts_requirement(self):
        # Randomly determine parts requirement category
        rand = np.random.random()
        if rand < self.parts_probabilities["basic"]:
            return "basic"
        elif rand < self.parts_probabilities["basic"] + self.parts_probabilities["medium"]:
            return "medium"
        else:
            return "major"

    def calculate_customer_satisfaction(self, wait_days):
        # Calculate satisfaction based on wait time
        if wait_days <= self.max_acceptable_wait_days:
            satisfaction = 1.0 - (wait_days * self.satisfaction_decay_per_day)
        else:
            satisfaction = max(0.2, 1.0 - (wait_days * self.satisfaction_decay_per_day))
        return max(0, min(1, satisfaction))

    def simulate(self, num_mechanics_per_month, num_years=1):
        # Initialize results storage
        results = {
            "daily_requests": [], "queue_length": [], "wait_times": [],
            "daily_revenue": [], "daily_costs": [], "daily_profit": [], "daily_invoice_amount": [],
            "customer_satisfaction": [], "mechanic_utilization": [],
            "date": [], "month": [], "repairs_completed": [], "repairs_requested": []
        }

        # Initialize simulation state
        day_of_year = 0
        queue = []  # List of tuples (arrival_day, repair_time, parts_cost)

        # Run simulation for specified number of years
        for year in range(num_years):
            for month in range(12):
                num_mechanics = num_mechanics_per_month[month]
                daily_capacity = num_mechanics * self.working_hours_per_day

                for day in range(self.days_in_month[month]):
                    # Generate random precipitation for the day
                    precipitation = np.random.normal(
                        self.monthly_avg_precipitation[month]/self.days_in_month[month],
                        self.monthly_avg_precipitation[month]/100 # std 1% avg precipitation for the day
                    )

                    # Generate repair requests for the day
                    daily_requests = self.generate_daily_repair_requests(month, precipitation)

                    # Add new requests to queue
                    for _ in range(daily_requests):
                        repair_time = self.generate_repair_time()
                        parts_category = self.determine_parts_requirement()
                        parts_cost = self.parts_costs[parts_category]
                        queue.append((day_of_year, repair_time, parts_cost))

                    # Process repairs for the day
                    repairs_completed = 0
                    revenue = 0
                    invoice_amount = 0
                    remaining_capacity = daily_capacity
                    wait_times = []

                    # Process queue until capacity is reached
                    queue.sort(key=lambda x: x[0])  # Sort by arrival day (FIFO)
                    new_queue = []

                    # Initialize a temporary list to collect all satisfaction scores for the current day
                    daily_satisfaction_scores = []

                    for request in queue:
                        arrival_day, repair_time, parts_cost = request

                        if repair_time <= remaining_capacity:
                            # Complete this repair
                            remaining_capacity -= repair_time
                            repairs_completed += 1
                            wait_time = day_of_year - arrival_day
                            wait_times.append(wait_time)

                            # Calculate revenue and satisfaction
                            price_modifier = 1.0 + np.random.normal(0, 0.15)  # Random price variation
                            repair_price = self.repair_price_average * price_modifier
                            revenue += repair_price # - parts_cost # Part costs should be forwarded to customer
                            invoice_amount += repair_price + parts_cost

                            # Add satisfaction score to daily collection instead of results
                            daily_satisfaction_scores.append(
                                self.calculate_customer_satisfaction(wait_time)
                            )
                        else:
                            # Cannot complete this repair today
                            new_queue.append(request)

                            # If queue is getting too long, customers might go elsewhere
                            if len(new_queue) > self.max_queue_size and np.random.random() < 0.2:
                                continue

                    # Update queue
                    queue = new_queue

                    # Calculate costs and profits
                    daily_labor_cost = num_mechanics * self.mechanic_salary_per_day
                    daily_profit = revenue - daily_labor_cost

                    # Calculate mechanic utilization
                    if daily_capacity > 0:
                        utilization = (daily_capacity - remaining_capacity) / daily_capacity
                    else:
                        utilization = 0

                    # Record results
                    results["daily_requests"].append(daily_requests)
                    results["queue_length"].append(len(queue))
                    results["daily_revenue"].append(revenue)
                    results["daily_costs"].append(daily_labor_cost)
                    results["daily_profit"].append(daily_profit)
                    results["daily_invoice_amount"].append(invoice_amount)
                    results["mechanic_utilization"].append(utilization)
                    results["date"].append(f"{year+1}-{month+1}-{day+1}")
                    results["month"].append(month)
                    results["repairs_completed"].append(repairs_completed)
                    results["repairs_requested"].append(daily_requests)

                    if wait_times:
                        results["wait_times"].append(np.mean(wait_times))
                    else:
                        results["wait_times"].append(0)

                    if daily_satisfaction_scores:
                        avg_daily_satisfaction = np.mean(daily_satisfaction_scores)
                    else:
                        avg_daily_satisfaction = 0.0  # No customers that day

                    results["customer_satisfaction"].append(avg_daily_satisfaction)
                    day_of_year += 1

        with open(f'bike_repair_shop_results_{datetime.timestamp(datetime.now())}.json', "w") as f:
            f.write(json.dumps(results))

        return pd.DataFrame(results)

    def analyze_results(self, df, num_mechanics_per_month):
        # Calculate monthly aggregated metrics
        monthly_metrics = df.groupby('month').agg({
            'daily_profit': 'sum',
            'daily_revenue': 'sum',
            'daily_costs': 'sum',
            'wait_times': 'mean',
            'customer_satisfaction': 'mean',
            'mechanic_utilization': 'mean',
            'repairs_completed': 'sum',
            'repairs_requested': 'sum',
            'queue_length': 'mean'
        }).reset_index()

        monthly_metrics['month_name'] = monthly_metrics['month'].apply(lambda x: self.month_names[x])
        monthly_metrics['mechanics'] = monthly_metrics['month'].apply(lambda x: num_mechanics_per_month[x])

        # Calculate total profit and other annual metrics
        total_profit = monthly_metrics['daily_profit'].sum()
        avg_satisfaction = monthly_metrics['customer_satisfaction'].mean()
        avg_wait_time = monthly_metrics['wait_times'].mean()

        print(f"Total Annual Profit: €{total_profit:.2f}")
        print(f"Average Customer Satisfaction: {avg_satisfaction:.2%}")
        print(f"Average Wait Time: {avg_wait_time:.1f} days")

        # Visualization
        fig, axs = plt.subplots(2, 2, figsize=(15, 10))

        # Plot 1: Profit by Month
        axs[0, 0].bar(monthly_metrics['month_name'], monthly_metrics['daily_profit'])
        axs[0, 0].set_title('Monthly Profit')
        axs[0, 0].set_xlabel('Month')
        axs[0, 0].set_ylabel('Profit (€)')

        # Plot 2: Mechanic Utilization
        axs[0, 1].plot(monthly_metrics['month_name'], monthly_metrics['mechanic_utilization'], marker='o')
        axs[0, 1].set_title('Monthly Mechanic Utilization')
        axs[0, 1].set_xlabel('Month')
        axs[0, 1].set_ylabel('Utilization Rate')
        axs[0, 1].grid(True)

        # Plot 3: Customer Wait Times
        axs[1, 0].plot(monthly_metrics['month_name'], monthly_metrics['wait_times'], marker='s')
        axs[1, 0].set_title('Average Wait Times')
        axs[1, 0].set_xlabel('Month')
        axs[1, 0].set_ylabel('Wait Time (days)')
        axs[1, 0].grid(True)

        # Plot 4: Repairs Requested vs. Completed
        axs[1, 1].bar(monthly_metrics['month_name'], monthly_metrics['repairs_requested'],
                      label='Requested', alpha=0.7)
        axs[1, 1].bar(monthly_metrics['month_name'], monthly_metrics['repairs_completed'],
                      label='Completed', alpha=0.7)
        axs[1, 1].set_title('Monthly Repair Volume')
        axs[1, 1].set_xlabel('Month')
        axs[1, 1].set_ylabel('Number of Repairs')
        axs[1, 1].legend()

        plt.tight_layout()
        plt.savefig(f'bike_repair_shop_results_{datetime.timestamp(datetime.now())}.png')
        plt.show()

        return monthly_metrics

# Run the simulation with different staffing scenarios
if __name__ == "__main__":
    np.random.seed(42)  # For reproducibility
    simulation = BikeRepairShopSimulation()

    # Scenario 1: Constant staffing
    print("Scenario 1: Constant staffing (3 mechanics all year)")
    constant_mechanics = [3] * 12
    results1 = simulation.simulate(constant_mechanics)
    metrics1 = simulation.analyze_results(results1, constant_mechanics)

    # Scenario 2: Seasonal staffing
    print("\nScenario 2: Seasonal staffing")
    seasonal_mechanics = [
        2, 2,  # Winter (Jan, Feb)
        3, 4, 5,  # Spring (Mar, Apr, May)
        6, 6, 5,  # Summer (Jun, Jul, Aug)
        4, 3, 2,  # Fall (Sep, Oct, Nov)
        2  # Winter (Dec)
    ]
    results2 = simulation.simulate(seasonal_mechanics)
    metrics2 = simulation.analyze_results(results2, seasonal_mechanics)
