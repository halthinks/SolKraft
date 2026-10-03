### `hf models` — Interact with models on the Hub.

- `hf models card MODEL_ID` — Get the model card (README) for a model on the Hub. `[--metadata --text --format [auto|human|agent|json|quiet]]`
- `hf models info MODEL_ID` — Get info about a model on the Hub. `[--revision TEXT --expand TEXT --format [auto|human|agent|json|quiet]]`
- `hf models list` — List models on the Hub, or files in a model repo. `[--search TEXT --author TEXT --filter TEXT --pipeline-tag TEXT --gated --apps TEXT --num-parameters TEXT --inference-provider [baseten|cerebras|cohere|deepinfra|fal-ai|featherless-ai|fireworks-ai|groq|hf-inference|novita|nscale|openai|ovhcloud|publicai|replicate|scaleway|together|wavespeed|zai-org] --warm --sort [created_at|downloads|last_modified|likes|trending_score] --limit INTEGER --expand TEXT --human-readable --tree --recursive --revision TEXT --format [auto|human|agent|json|quiet]]`
