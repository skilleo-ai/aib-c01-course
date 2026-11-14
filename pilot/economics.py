"""Reproducible fictional teaching model, not an AWS pricing estimator."""
import json

def calculate(coverage=.5, realization=.7):
    if not 0 <= coverage <= 1 or not 0 <= realization <= 1:
        raise ValueError('fractions must be within [0,1]')
    hours=12000*coverage*3/60
    monthly=hours*30*realization
    cost=12*3000+18000
    net=12*monthly-cost
    return {'coverage':coverage,'realization':realization,'released_hours_month':hours,'recognized_value_month':monthly,'annual_benefit':12*monthly,'year_one_cost':cost,'year_one_net':net,'roi':net/cost,'simple_payback_months':18000/(monthly-3000) if monthly>3000 else None}

if __name__=='__main__':
    print(json.dumps([calculate(v) for v in [.25,.5,.75]],indent=2))
