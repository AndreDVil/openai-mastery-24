cd C:\GitHub\openai-mastery-24
.venv\Scripts\Activate.ps1

cd projects\p04_multi_model_token_cost_analyzer
$env:PYTHONPATH="src"

python -m scripts.run_benchmark
