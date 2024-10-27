import time
import pandas as pd
import duckdb
from sympy import isprime
from datetime import datetime

def calculate_mersenne_primes(runtime_minutes: int):
    # Convert minutes to seconds
    runtime_seconds = runtime_minutes * 60
    end_time = time.time() + runtime_seconds
    
    # Initialize the list to store Mersenne primes and elapsed time
    mersenne_primes = []
    p = 2  # Start from the first prime number
    last_prime_time = time.time()

    # Iterate while within the allowed time limit
    while time.time() < end_time:
        # Calculate the Mersenne prime candidate
        mersenne_candidate = 2 ** p - 1
        
        # Check if the Mersenne candidate is prime
        if isprime(mersenne_candidate):
            current_time = time.time()
            elapsed_time = current_time - last_prime_time
            mersenne_primes.append({
                "p": p, 
                "primes": str(mersenne_candidate),  # Convert Mersenne Prime to string
                "prime_length": len(str(mersenne_candidate)),  # Count characters in Mersenne Prime
                "elapsed_time": elapsed_time  # Time since last prime found
            })
            last_prime_time = current_time
        
        # Move to the next prime number for p
        p += 1
        # Ensure p itself is prime
        while not isprime(p):
            p += 1

    # Capture the completion timestamp
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a DataFrame from the Mersenne primes list
    df = pd.DataFrame(mersenne_primes)
    
    # Add runtime and completion timestamp as additional columns
    df['runtime_minutes'] = runtime_minutes
    df['completion_timestamp'] = completion_time

    # Write DataFrame to CSV
    df.to_csv("mersenne_primes_elasped.csv", index=False)
    
    # Write DataFrame to DuckDB and append to existing table with Mersenne Prime as string
    conn = duckdb.connect("mersenne_primes_py.duckdb")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS mersenne_primes (
            p INTEGER,
            primes STRING,
            prime_length INTEGER,
            elapsed_time DOUBLE,
            runtime_minutes INTEGER,
            completion_timestamp TIMESTAMP
        )
    """)
    conn.execute("INSERT INTO mersenne_primes SELECT * FROM df")
    conn.close()

    return df

# Run the function for a specified time limit (in minutes)
runtime_minutes = int(input("Enter runtime in minutes: "))
df_result = calculate_mersenne_primes(runtime_minutes)
print(df_result)
