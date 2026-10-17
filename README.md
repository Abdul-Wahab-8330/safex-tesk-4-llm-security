
# LLM Security: Prompt Injection and Jailbreak Evaluation

A Python project that evaluates lightweight defenses against prompt injection and jailbreak attempts in a Gemini-powered assistant for an independent energy consultancy.

## Objectives

- Establish a baseline LLM evaluation.
- Detect known prompt-injection patterns with an input guard.
- Use a hardened system prompt to reinforce intended behavior.
- Check generated responses for known system-instruction leak signatures.
- Compare baseline and defended evaluation outcomes.
- Test security behavior and harmless inputs with automated regression tests.

## Architecture

User input
    |
    v
Input Guard
    |
    +---- Known pattern detected ----> blocked_input
    |
    v
Hardened System Prompt + Gemini
    |
    v
Output Guard
    |
    +---- Known leak signature ------> blocked_output
    |
    v
Return response: success

API and processing failures are recorded separately as api_error.

## Technology Stack

- Python
- Google Gen AI SDK
- Gemini API
- Regular expressions
- python-dotenv
- pandas
- Jupyter Notebook
- unittest

## Project Structure

- `notebooks/`: baseline experiments and defense development
- `src/llm_security/`: reusable security and API modules
- `tests/`: automated input- and output-guard tests
- `scripts/`: evaluation runner
- `data/`: attack dataset and saved evaluation results

## Setup

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the environment's Python directly instead.

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Use the same Python interpreter for installing dependencies and running the project.

### 3. Configure the API key

Copy `.env.example` to `.env` and replace the placeholder with your own Gemini API key.

Do not commit `.env` to version control.

### 4. Run automated tests

From the project root:

```powershell
python -m unittest discover -s tests -v
```

These tests do not call Gemini and do not require an API key.

### 5. Run the defended evaluation

From the project root:

```powershell
python scripts/run_evaluation.py
```

The script reads `data/attack_dataset.json` and writes the latest results to `data/defended_results.json`.

The evaluation makes real API calls for prompts that pass the input guard. API usage, quotas, model availability, and network errors may affect the run.

## Initial Evaluation Results

The initial eight-case evaluation produced the following defended outcomes:

| Outcome | Count |
|---|---:|
| `blocked_input` | 6 |
| `success` | 2 |
| `blocked_output` | 0 |
| `api_error` | 0 |
| **Total** | **8** |

All six known attack prompts were blocked by the input guard, and both benign energy questions passed through the pipeline.

The local input-guard regression suite also passed 14/14 checks: six attack prompts, two benign dataset prompts, and six harmless diagnostic prompts.

The baseline returned successful API responses for all eight prompts. An API success status alone does not establish whether an attack succeeded or protected information was disclosed; baseline response content must be inspected separately.

These are results from a small, predefined dataset, not a comprehensive security assessment.

## Security Design

### Input guard
Uses regular-expression heuristics to identify known instruction overrides, role manipulation, and system-prompt extraction attempts.

### Hardened system prompt
Reinforces the assistant's role and directs it to reject conflicting requests.

### Output guard
Checks for a small set of known protected-instruction signatures.

### Evaluation and regression tests
Separates input blocks, output blocks, successful responses, and API errors so service failures are not counted as security successes.

## Limitations

- Regex filters can miss novel, obfuscated, multilingual, or indirect attacks.
- Legitimate requests may resemble attack patterns.
- A hardened system prompt is not a security boundary by itself.
- The output guard detects only known signatures and may miss paraphrased or partial disclosures.
- Passing these checks does not prove that a response is safe.
- The current dataset is small and does not establish production-level robustness.
- API responses and results can vary between model versions and runs.

This project is an educational security-testing prototype, not a production-ready defense system.

## Future Improvements

- Expand direct, indirect, obfuscated, and multilingual attack tests.
- Add more benign cases to measure false-positive behavior.
- Inspect baseline responses for actual instruction disclosure.
- Report detection rate, false-positive rate, and API-error rate separately.
- Add structured logging and reproducible evaluation reports.
- Evaluate additional model configurations and defense strategies.

## Responsible Use

Use the system to evaluate and improve LLM application security. Do not include real secrets or confidential information in test prompts or public evaluation artifacts.
