import random
import datetime

def generate_logs(filename="server_access.log", num_lines=5000):
    ips = [f"192.168.1.{i}" for i in range(1, 50)] + ["203.0.113.42"] * 150  # 203.0.113.42 is the attacker
    endpoints = ["/api/v1/users", "/api/v1/auth", "/index.html", "/images/logo.png"]
    methods = ["GET", "POST"]
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "curl/7.68.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    ]

    start_time = datetime.datetime.now() - datetime.timedelta(hours=2)

    with open(filename, "w") as f:
        for _ in range(num_lines):
            ip = random.choice(ips)
            method = random.choice(methods)
            endpoint = random.choice(endpoints)
            
            # Simulate attack from specific IP
            if ip == "203.0.113.42" and endpoint == "/api/v1/auth":
                status = 429 if random.random() > 0.2 else 500
                method = "POST"
            else:
                status = 200 if random.random() > 0.05 else 404

            timestamp = start_time.strftime("%d/%b/%Y:%H:%M:%S +0000")
            ua = random.choice(user_agents)
            
            # Apache/Nginx combined log format
            log_line = f'{ip} - - [{timestamp}] "{method} {endpoint} HTTP/1.1" {status} {random.randint(200, 5000)} "-" "{ua}"\n'
            f.write(log_line)
            
            # Advance time slightly
            start_time += datetime.timedelta(seconds=random.randint(1, 5))

    print(f"Generated {num_lines} log lines in {filename}.")

if __name__ == "__main__":
    generate_logs()
