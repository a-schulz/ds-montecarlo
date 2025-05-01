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
        self.queue_leave_probability = 0.2  # probability of leaving if queue is too long

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
            # Set minimum satisfaction to 0.2 if wait time exceeds max acceptable
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
                        if len(queue) > self.max_queue_size and np.random.random() < self.queue_leave_probability:
                            continue
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
                            # If queue is getting too long, customers might go elsewhere
                            if len(new_queue) > self.max_queue_size and np.random.random() < self.queue_leave_probability:
                                continue
                            new_queue.append(request)


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
        fig, axs = plt.subplots(3, 2, figsize=(15, 10))

        # Plot 1: Profit by Month
        axs[0, 0].bar(monthly_metrics['month_name'], monthly_metrics['daily_profit'])
        axs[0, 0].set_title('Monthly Profit')
        axs[0, 0].set_xlabel('Month')
        axs[0, 0].set_ylabel('Profit (€)')

        # Plot 2: Repairs Requested vs. Completed
        axs[0, 1].bar(monthly_metrics['month_name'], monthly_metrics['repairs_requested'],
                      label='Requested', alpha=0.7)
        axs[0, 1].bar(monthly_metrics['month_name'], monthly_metrics['repairs_completed'],
                      label='Completed', alpha=0.7)
        axs[0, 1].set_title('Monthly Repair Volume')
        axs[0, 1].set_xlabel('Month')
        axs[0, 1].set_ylabel('Number of Repairs')
        axs[0, 1].legend()

        # Plot 3: Customer Wait Times
        axs[1, 0].plot(monthly_metrics['month_name'], monthly_metrics['wait_times'], marker='s')
        axs[1, 0].set_title('Average Wait Times')
        axs[1, 0].set_xlabel('Month')
        axs[1, 0].set_ylabel('Wait Time (days)')
        axs[1, 0].grid(True)


        # Plot 4: Mechanic Utilization
        axs[1, 1].plot(monthly_metrics['month_name'], monthly_metrics['mechanic_utilization'], marker='o')
        axs[1, 1].set_title('Monthly Mechanic Utilization')
        axs[1, 1].set_xlabel('Month')
        axs[1, 1].set_ylabel('Utilization Rate')
        axs[1, 1].grid(True)

        # Plot 5: Customer Satisfaction
        axs[2, 0].plot(monthly_metrics['month_name'], monthly_metrics['customer_satisfaction'], marker='o', color='orange')
        axs[2, 0].set_title('Customer Satisfaction Over the Year')
        axs[2, 0].set_xlabel('Month')
        axs[2, 0].set_ylabel('Satisfaction Rate')
        axs[2, 0].grid(True)
        axs[2, 0].set_ylim(0, 1)
        for i, v in enumerate(monthly_metrics['customer_satisfaction']):
            axs[2, 0].text(i, v + 0.02, f"{v:.2%}", ha='center', va='bottom')
        axs[2, 0].set_xticks(range(len(monthly_metrics['month_name'])))
        axs[2, 0].set_xticklabels(monthly_metrics['month_name'], rotation=45)
        axs[2, 0].set_yticks(np.arange(0, 1.1, 0.1))
        axs[2, 0].set_yticklabels([f"{int(v*100)}%" for v in np.arange(0, 1.1, 0.1)])
        axs[2, 0].legend(['Customer Satisfaction'])

        # Plot 6: Queue Length
        axs[2, 1].plot(monthly_metrics['month_name'], monthly_metrics['queue_length'], marker='d', color='purple')
        axs[2, 1].set_title('Average Queue Length Over the Year')
        axs[2, 1].set_xlabel('Month')
        axs[2, 1].set_ylabel('Queue Length')
        axs[2, 1].grid(True)

        plt.tight_layout()
        plt.savefig(f'bike_repair_shop_results_{datetime.timestamp(datetime.now())}.png')
        plt.show()

        return monthly_metrics

    def calculate_optimal_mechanics(self, run_simulation=True, max_mechanics=20, min_mechanics=1):
        """
        Calculate optimal number of mechanics per month based on expected demand and profitability.
        
        Args:
            run_simulation (bool): Whether to run a simulation with the calculated configuration
            max_mechanics (int): Maximum number of mechanics to consider per month
            min_mechanics (int): Minimum number of mechanics to consider per month
            
        Returns:
            list: Estimated optimal number of mechanics for each month
        """
        optimal_mechanics = []
        
        print("Calculating optimal mechanics per month...")
        
        for month in range(12):
            # Base repair requests for this month
            base_requests = self.monthly_base_repairs[month]
            
            # Calculate expected work hours needed
            expected_daily_requests = base_requests
            expected_repair_hours = expected_daily_requests * self.repair_time_mean
            
            # Calculate mechanics needed (add 10% buffer for variability)
            mechanics_needed = expected_repair_hours / self.working_hours_per_day * 1.1
            
            # Find the most profitable number of mechanics
            best_profit = float('-inf')
            best_count = min_mechanics
            
            for count in range(min_mechanics, max_mechanics + 1):
                # Daily capacity with this many mechanics
                daily_capacity = count * self.working_hours_per_day
                
                # Expected repairs completed (limited by capacity)
                repairs_completed = min(expected_daily_requests, 
                                       daily_capacity / self.repair_time_mean)
                
                # Expected revenue and cost
                expected_revenue = repairs_completed * self.repair_price_average
                daily_cost = count * self.mechanic_salary_per_day
                daily_profit = expected_revenue - daily_cost
                monthly_profit = daily_profit * self.days_in_month[month]
                
                # Factor in utilization and satisfaction
                utilization = min(1.0, expected_repair_hours / daily_capacity) if daily_capacity > 0 else 1.0
                
                # If utilization is too high, customer satisfaction drops and we lose business
                if utilization > 0.9:
                    satisfaction_penalty = (utilization - 0.9) * 2000  # Simple penalty model
                    monthly_profit -= satisfaction_penalty
                
                if monthly_profit > best_profit:
                    best_profit = monthly_profit
                    best_count = count
            
            optimal_mechanics.append(best_count)
            
            # Calculate metrics for the chosen count
            daily_capacity = best_count * self.working_hours_per_day
            utilization = min(1.0, expected_repair_hours / daily_capacity) if daily_capacity > 0 else 1.0
            repairs_completed = min(expected_daily_requests, daily_capacity / self.repair_time_mean)
            expected_revenue = repairs_completed * self.repair_price_average
            daily_cost = best_count * self.mechanic_salary_per_day
            monthly_profit = (expected_revenue - daily_cost) * self.days_in_month[month]
            
            print(f"Month {self.month_names[month]}: {best_count} mechanics " 
                  f"(Utilization: {utilization:.2%}, Est. monthly profit: €{monthly_profit:.2f})")
        
        print(f"Calculated optimal mechanics configuration: {optimal_mechanics}")
        
        # Run simulation with this configuration if requested
        if run_simulation:
            print("\nRunning simulation with calculated optimal configuration...")
            results = self.simulate(optimal_mechanics)
            metrics = self.analyze_results(results, optimal_mechanics)
        
        return optimal_mechanics

# Run the simulation with different staffing scenarios
if __name__ == "__main__":
    np.random.seed(42)  # For reproducibility
    simulation = BikeRepairShopSimulation()
    
    # Original scenarios below
    # Scenario 1: Constant staffing
    print("\nScenario 1: Constant staffing (5 mechanics all year)")
    constant_mechanics = [5] * 12
    results1 = simulation.simulate(constant_mechanics)
    metrics1 = simulation.analyze_results(results1, constant_mechanics)

    # # Scenario 2: Seasonal staffing (intuitively defined)
    # print("\nScenario 2: Seasonal staffing")
    # seasonal_mechanics = [
    #     2, 2,  # Winter (Jan, Feb)
    #     3, 4, 5,  # Spring (Mar, Apr, May)
    #     6, 6, 5,  # Summer (Jun, Jul, Aug)
    #     4, 3, 2,  # Fall (Sep, Oct, Nov)
    #     2  # Winter (Dec)
    # ]
    # results2 = simulation.simulate(seasonal_mechanics)
    # metrics2 = simulation.analyze_results(results2, seasonal_mechanics)

    # Calculate optimal mechanics configuration
    print("Calculating optimal mechanics configuration:")
    optimal_mechanics = simulation.calculate_optimal_mechanics(False)

    # Scenario 3: Optimal staffing
    print("\nScenario 3: Optimal staffing")
    results3 = simulation.simulate(optimal_mechanics)
    metrics3 = simulation.analyze_results(results3, optimal_mechanics)