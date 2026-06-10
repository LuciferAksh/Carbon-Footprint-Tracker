# Community 2: main.py, generate_challenge_prompt, parse_challenge_response

> 52 nodes · cohesion 0.05

## Key Concepts

- **parse_challenge_response()** (9 connections) — `functions\challenge_generator.py`
- **TestGenerateChallengePrompt** (9 connections) — `functions\tests\test_challenge_generator.py`
- **TestParseChallengeResponse** (9 connections) — `functions\tests\test_challenge_generator.py`
- **generate_challenge_prompt()** (8 connections) — `functions\challenge_generator.py`
- **._sample_profile()** (6 connections) — `functions\tests\test_challenge_generator.py`
- **main.py** (5 connections) — `backend\app\main.py`
- **._sample_logs()** (5 connections) — `functions\tests\test_challenge_generator.py`
- **.test_prompt_contains_log_summary()** (5 connections) — `functions\tests\test_challenge_generator.py`
- **.test_prompt_contains_profile_info()** (5 connections) — `functions\tests\test_challenge_generator.py`
- **.test_prompt_identifies_highest_category()** (5 connections) — `functions\tests\test_challenge_generator.py`
- **_call_gemini_for_challenge()** (4 connections) — `functions\main.py`
- **generate_weekly_challenges()** (4 connections) — `functions\main.py`
- **.test_prompt_handles_empty_logs()** (4 connections) — `functions\tests\test_challenge_generator.py`
- **.test_parses_json_in_code_block()** (4 connections) — `functions\tests\test_challenge_generator.py`
- **.test_parses_valid_json()** (4 connections) — `functions\tests\test_challenge_generator.py`
- **._valid_response()** (4 connections) — `functions\tests\test_challenge_generator.py`
- **challenge_generator.py** (3 connections) — `functions\challenge_generator.py`
- **main.py** (3 connections) — `functions\main.py`
- **test_challenge_generator.py** (3 connections) — `functions\tests\test_challenge_generator.py`
- **lifespan()** (3 connections) — `backend\app\main.py`
- **.test_prompt_handles_missing_profile_fields()** (3 connections) — `functions\tests\test_challenge_generator.py`
- **.test_coerces_co2_saving_to_float()** (3 connections) — `functions\tests\test_challenge_generator.py`
- **.test_handles_invalid_category()** (3 connections) — `functions\tests\test_challenge_generator.py`
- **.test_handles_invalid_json()** (3 connections) — `functions\tests\test_challenge_generator.py`
- **.test_rejects_missing_fields()** (3 connections) — `functions\tests\test_challenge_generator.py`
- *... and 27 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `backend\app\main.py`
- `functions\challenge_generator.py`
- `functions\main.py`
- `functions\tests\test_challenge_generator.py`

## Audit Trail

- EXTRACTED: 118 (81%)
- INFERRED: 27 (19%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*