import json
class Estimate:
    def __init__(self, avg_est, avg_lb, avg_ub, count_est, count_lb, count_ub, rate, cost, prob: float=0) -> None:
        self.avg = avg_est
        self.avg_lb = avg_lb
        self.avg_ub = avg_ub
        self.count = count_est / rate
        self.count_lb = count_lb / rate
        self.count_ub = count_ub / rate
        self.rate = rate
        self.cost = cost
        self.prob = prob

    def log(self):
        print(f"rate: {self.rate}, cost: {self.cost}")
        print(f"count: {self.count} ({self.count_lb}, {self.count_ub})")
        print(f"avg: {self.avg} ({self.avg_lb}, {self.avg_ub})")


    
    def save(self, file: str):
        with open(file, "a+") as f:
            output_dict = {
                "rate": self.rate,
                "cost": self.cost,
                "avg": self.avg,
                "avg_lb": self.avg_lb,
                "avg_ub": self.avg_ub,
                "count": self.count,
                "count_lb": self.count_lb,
                "count_ub": self.count_ub,
                "prob": self.prob
            }
            output_str = json.dumps(output_dict)
            f.write(output_str + '\n')
