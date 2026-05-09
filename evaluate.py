import json, statistics, sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.pipeline import AppCompiler

compiler = AppCompiler()
with open(os.path.join(os.path.dirname(__file__), 'prompts.json')) as f:
    prompts = json.load(f)

results = []
for p in prompts:
    r = compiler.compile(p)
    results.append({
        'prompt': p,
        'success': r.metrics['success'],
        'latency_ms': r.metrics['latency_ms'],
        'repair_attempts': r.repair_attempts,
        'error_count': r.metrics['error_count'],
        'warning_count': r.metrics['warning_count']
    })

summary = {
    'total': len(results),
    'success_rate': sum(x['success'] for x in results) / len(results),
    'avg_latency_ms': round(statistics.mean(x['latency_ms'] for x in results), 2),
    'avg_repairs': round(statistics.mean(x['repair_attempts'] for x in results), 2),
    'results': results
}
print(json.dumps(summary, indent=2))
