"""
Data Analysis Project: COVID-19 Data Analysis

This project analyzes COVID-19 data to extract insights about:
- Global and country-specific infection trends
- Vaccination effectiveness
- Correlation between social factors and infection rates
- Visualization of pandemic spread over time

Libraries used:
- pandas: Data manipulation and analysis
- numpy: Numerical operations
- matplotlib & seaborn: Data visualization
- scikit-learn: Simple predictive modeling
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import os
from datetime import datetime, timedelta


class COVIDDataAnalyzer:
    """Class for analyzing COVID-19 data"""
    
    def __init__(self, data_dir="data"):
        """Initialize the analyzer with paths to data files"""
        self.data_dir = data_dir
        self.cases_df = None
        self.deaths_df = None
        self.vaccinations_df = None
        self.population_df = None
        self.merged_df = None
        self.load_data()
    
    def load_data(self):
        """Load data from CSV files"""
        print("Loading COVID-19 data...")
        
        # Check if data directory exists, if not create it
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print(f"Created directory: {self.data_dir}")
            print("Please download the dataset files into this directory.")
            print("Dataset links:")
            print("- Cases: https://covid.ourworldindata.org/data/owid-covid-data.csv")
            print("- Vaccinations: https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv")
            print("- Population: https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2019_TotalPopulationBySex.csv")
            return
        
        try:
            # Load COVID-19 cases/deaths data
            cases_path = os.path.join(self.data_dir, "owid-covid-data.csv")
            if os.path.exists(cases_path):
                self.cases_df = pd.read_csv(cases_path)
                print(f"Loaded cases data: {self.cases_df.shape[0]} rows, {self.cases_df.shape[1]} columns")
            else:
                print(f"Warning: {cases_path} not found")
            
            # Load vaccination data
            vax_path = os.path.join(self.data_dir, "vaccinations.csv")
            if os.path.exists(vax_path):
                self.vaccinations_df = pd.read_csv(vax_path)
                print(f"Loaded vaccination data: {self.vaccinations_df.shape[0]} rows, {self.vaccinations_df.shape[1]} columns")
            else:
                print(f"Warning: {vax_path} not found")
            
            # Load population data
            pop_path = os.path.join(self.data_dir, "population_data.csv")
            if os.path.exists(pop_path):
                self.population_df = pd.read_csv(pop_path)
                print(f"Loaded population data: {self.population_df.shape[0]} rows, {self.population_df.shape[1]} columns")
            else:
                print(f"Warning: {pop_path} not found")
                
            self.preprocess_data()
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
    
    def preprocess_data(self):
        """Preprocess and merge datasets"""
        if self.cases_df is None:
            print("No data available for preprocessing")
            return
        
        print("Preprocessing data...")
        
        # Convert date columns to datetime
        if 'date' in self.cases_df.columns:
            self.cases_df['date'] = pd.to_datetime(self.cases_df['date'])
        
        if self.vaccinations_df is not None and 'date' in self.vaccinations_df.columns:
            self.vaccinations_df['date'] = pd.to_datetime(self.vaccinations_df['date'])
        
        # Merge vaccination data with cases if both are available
        if self.vaccinations_df is not None:
            print("Merging vaccination and cases data...")
            # Simplified merge example - in a real scenario you'd need more sophisticated merging
            self.merged_df = self.cases_df.copy()
            
            # Example of creating per capita columns
            if 'population' in self.cases_df.columns:
                if 'total_cases' in self.cases_df.columns:
                    self.merged_df['cases_per_million'] = self.cases_df['total_cases'] * 1000000 / self.cases_df['population']
                if 'total_deaths' in self.cases_df.columns:
                    self.merged_df['deaths_per_million'] = self.cases_df['total_deaths'] * 1000000 / self.cases_df['population']
        
        print("Preprocessing complete")
    
    def display_global_trends(self):
        """Display global COVID-19 trends"""
        if self.cases_df is None:
            print("No data available for analysis")
            return
        
        print("\n=== Global COVID-19 Trends ===")
        
        # Group by date and sum cases and deaths
        if 'date' in self.cases_df.columns and 'new_cases' in self.cases_df.columns:
            global_daily = self.cases_df.groupby('date')[['new_cases', 'new_deaths']].sum().reset_index()
            
            # Calculate 7-day rolling average
            global_daily['cases_7day_avg'] = global_daily['new_cases'].rolling(7).mean()
            global_daily['deaths_7day_avg'] = global_daily['new_deaths'].rolling(7).mean()
            
            print("Global daily cases (7-day rolling average):")
            latest_data = global_daily.tail(1)
            print(f"Latest date: {latest_data['date'].iloc[0].strftime('%Y-%m-%d')}")
            print(f"New cases (7-day avg): {latest_data['cases_7day_avg'].iloc[0]:,.0f}")
            print(f"New deaths (7-day avg): {latest_data['deaths_7day_avg'].iloc[0]:,.0f}")
            
            # Plot global trends
            plt.figure(figsize=(12, 6))
            plt.plot(global_daily['date'], global_daily['cases_7day_avg'], label='7-Day Avg New Cases')
            plt.title('Global COVID-19 Cases (7-Day Rolling Average)')
            plt.xlabel('Date')
            plt.ylabel('Number of Cases')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.legend()
            
            # Save the plot
            plt.savefig(os.path.join(self.data_dir, 'global_cases_trend.png'))
            print(f"Plot saved to {os.path.join(self.data_dir, 'global_cases_trend.png')}")
            plt.close()
    
    def analyze_country(self, country):
        """Analyze data for a specific country"""
        if self.cases_df is None:
            print("No data available for analysis")
            return
        
        print(f"\n=== COVID-19 Analysis for {country} ===")
        
        # Filter data for the specified country
        country_data = self.cases_df[self.cases_df['location'] == country]
        
        if country_data.empty:
            print(f"No data found for {country}")
            return
        
        # Display summary for the country
        latest = country_data.iloc[-1]
        print(f"Latest data as of {latest['date'].strftime('%Y-%m-%d')}:")
        
        if 'total_cases' in latest and not pd.isna(latest['total_cases']):
            print(f"Total cases: {latest['total_cases']:,.0f}")
        
        if 'total_deaths' in latest and not pd.isna(latest['total_deaths']):
            print(f"Total deaths: {latest['total_deaths']:,.0f}")
        
        if 'people_vaccinated' in latest and not pd.isna(latest['people_vaccinated']):
            print(f"People vaccinated: {latest['people_vaccinated']:,.0f}")
        
        if 'people_fully_vaccinated' in latest and not pd.isna(latest['people_fully_vaccinated']):
            print(f"People fully vaccinated: {latest['people_fully_vaccinated']:,.0f}")
        
        # Plot cases and deaths for the country
        if 'new_cases_smoothed' in country_data.columns and 'new_deaths_smoothed' in country_data.columns:
            fig, ax1 = plt.subplots(figsize=(12, 6))
            
            # Plot new cases
            ax1.set_xlabel('Date')
            ax1.set_ylabel('New Cases', color='tab:blue')
            ax1.plot(country_data['date'], country_data['new_cases_smoothed'], color='tab:blue', label='New Cases (7-day avg)')
            ax1.tick_params(axis='y', labelcolor='tab:blue')
            
            # Create second y-axis for deaths
            ax2 = ax1.twinx()
            ax2.set_ylabel('New Deaths', color='tab:red')
            ax2.plot(country_data['date'], country_data['new_deaths_smoothed'], color='tab:red', label='New Deaths (7-day avg)')
            ax2.tick_params(axis='y', labelcolor='tab:red')
            
            # Add legend
            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
            
            plt.title(f'COVID-19 Cases and Deaths in {country}')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            
            # Save the plot
            plt.savefig(os.path.join(self.data_dir, f'{country.lower().replace(" ", "_")}_trend.png'))
            print(f"Plot saved to {os.path.join(self.data_dir, f'{country.lower().replace(' ', '_')}_trend.png')}")
            plt.close()
    
    def vaccination_impact_analysis(self):
        """Analyze the impact of vaccination on case and death rates"""
        if self.merged_df is None or 'people_vaccinated_per_hundred' not in self.merged_df.columns:
            print("Vaccination data not available for analysis")
            return
        
        print("\n=== Vaccination Impact Analysis ===")
        
        # Select recent data 
        cutoff_date = datetime.now() - timedelta(days=30)
        recent_data = self.merged_df[self.merged_df['date'] >= cutoff_date]
        
        # Group by country and get the latest data
        latest_by_country = recent_data.sort_values('date').groupby('location').last().reset_index()
        
        # Filter countries with sufficient data
        filtered_countries = latest_by_country[
            (latest_by_country['population'] > 1000000) & 
            (latest_by_country['people_vaccinated_per_hundred'].notna()) &
            (latest_by_country['new_cases_per_million'].notna()) &
            (latest_by_country['new_deaths_per_million'].notna())
        ]
        
        if filtered_countries.shape[0] < 10:
            print("Insufficient data for meaningful vaccination impact analysis")
            return
        
        print(f"Analyzing vaccination impact using data from {filtered_countries.shape[0]} countries")
        
        # Create scatter plot
        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(
            filtered_countries['people_vaccinated_per_hundred'],
            filtered_countries['new_deaths_per_million'],
            c=filtered_countries['gdp_per_capita'],
            cmap='viridis',
            alpha=0.7,
            s=filtered_countries['population'] / 1000000,  # Size based on population
        )
        
        # Add colorbar
        cbar = plt.colorbar(scatter)
        cbar.set_label('GDP per Capita')
        
        # Add labels for some notable countries
        for idx, row in filtered_countries.iloc[::5].iterrows():  # Label every 5th country for clarity
            plt.annotate(
                row['location'],
                (row['people_vaccinated_per_hundred'], row['new_deaths_per_million']),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=8
            )
        
        # Add trendline
        if filtered_countries.shape[0] > 1:
            x = filtered_countries['people_vaccinated_per_hundred']
            y = filtered_countries['new_deaths_per_million']
            
            # Fit linear regression
            mask = ~np.isnan(x) & ~np.isnan(y)
            if np.sum(mask) > 1:
                model = LinearRegression()
                model.fit(x[mask].values.reshape(-1, 1), y[mask])
                
                # Plot regression line
                x_line = np.array([min(x), max(x)])
                y_line = model.predict(x_line.reshape(-1, 1))
                plt.plot(x_line, y_line, color='red', linestyle='--')
                
                # Calculate and display R²
                r2 = r2_score(y[mask], model.predict(x[mask].values.reshape(-1, 1)))
                plt.text(0.05, 0.95, f'R² = {r2:.2f}', transform=plt.gca().transAxes, 
                         fontsize=10, verticalalignment='top')
        
        plt.title('Vaccination Rates vs. Death Rates by Country')
        plt.xlabel('People Vaccinated (per hundred)')
        plt.ylabel('New Deaths (per million)')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(os.path.join(self.data_dir, 'vaccination_impact.png'))
        print(f"Plot saved to {os.path.join(self.data_dir, 'vaccination_impact.png')}")
        plt.close()
    
    def generate_report(self):
        """Generate a comprehensive COVID-19 analysis report"""
        if self.cases_df is None:
            print("No data available for report generation")
            return
            
        print("\n=== COVID-19 Analysis Report ===")
        
        # Global trends
        self.display_global_trends()
        
        # Country-specific analysis for top 5 countries by total cases
        if 'location' in self.cases_df.columns and 'total_cases' in self.cases_df.columns:
            top_countries = self.cases_df.groupby('location')['total_cases'].max().nlargest(5).index.tolist()
            for country in top_countries:
                self.analyze_country(country)
        
        # Vaccination impact analysis
        self.vaccination_impact_analysis()
        
        print("\nReport generation complete. All plots saved to the data directory.")


# Example usage
if __name__ == "__main__":
    analyzer = COVIDDataAnalyzer()
    if analyzer.cases_df is not None:
        # Generate the report
        analyzer.generate_report()
        
        # If you want to analyze a specific country
        # analyzer.analyze_country("United States")
    else:
        print("\nPlease download the required datasets into the 'data' directory to proceed with the analysis.")
        print("See the loading message above for the specific files needed.")