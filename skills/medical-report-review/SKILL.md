---
name: medical-report-review
description: Review user-provided or previously shared medical reports, extract key values, compare against current symptoms, and suggest safe follow-up questions/checks without diagnosing.
---

# Medical Report Review

Use this skill when the user asks to interpret, compare, or recover prior medical reports/checkups/lab results, especially when current symptoms may relate to prior findings.

## Core stance

- Be clinically cautious: explain possibilities and next steps, not a definitive diagnosis.
- Ground every report-specific claim in an actual report value, user-provided image/PDF/text, or located local artifact.
- Prefer the user's stated medical-report preference: first say what prior tests already make less likely or partially rule out, then say what remains unresolved and what to check next.
- If the user reports urgent red flags, recommend urgent/emergency care before deep report analysis.

## Workflow

1. **Clarify the current symptom and acuity**
   - Ask/identify red flags only if not already known.
   - For visible blood in urine, chest pain, neuro deficits, severe pain, fever/chills, inability to urinate, syncope, etc., prioritize timely care.

2. **Recover or inspect source reports**
   - Use current attachments first.
   - If the user says the report was shared before, search session history and local agent artifacts rather than asking them to resend immediately.
   - For OpenClaw/Hermes history, see `references/local-report-recovery.md`.

3. **Extract only relevant values**
   - Include date/source, item name, result, unit, and reference range when available.
   - Do not dump unrelated personal or medical details.
   - Separate abnormal findings from normal/reassuring findings.

4. **Interpret by differential pathway**
   - For each symptom, map prior findings to what they reduce likelihood of vs what they do not exclude.
   - Example for hematuria: urine protein, urine sediment RBCs, WBC/nitrite, casts, creatinine/eGFR, ultrasound/CT findings, and current gross vs microscopic blood determine nephrology vs urology emphasis.

5. **Recommend next practical step**
   - Give a short prioritized list: department, first repeat tests, and escalation tests if initial results confirm concern.
   - Mention limitations clearly: old normal tests may not rule out a new episode.

## Hematuria quick frame

When reviewing blood/possible blood in urine:

- Gross visible red/tea-colored urine is more urgent than a prior borderline microscopic result.
- Prior normal creatinine/eGFR and negative urine protein reduce concern for obvious kidney-function loss or proteinuric glomerular disease, but do not rule out a new episode.
- Dipstick occult blood with few/no RBCs on microscopy can reflect false positives, hemoglobin/myoglobin, timing/sample issues, or lysed RBCs; repeat urine microscopy matters.
- Infection is less supported when leukocyte esterase, nitrite, and urine WBC are negative, but symptoms and culture may still guide.
- Ultrasound can miss small stones, ureteral lesions, and some bladder/upper-tract pathology; persistent or gross painless hematuria often needs urology assessment and possibly CT/CTU/cystoscopy.

## Response format

Keep it compact and useful:

- **找到的既往结果**: bullet list with values.
- **这些结果能说明/降低怀疑的点**: what is partly ruled out.
- **仍不能排除的点**: what current symptoms require rechecking.
- **下一步**: department + prioritized tests + urgent red flags.

## Pitfalls

- Do not say a past normal ultrasound or kidney function test makes current gross hematuria safe to ignore.
- Do not treat `尿隐血 3+` and `尿红细胞 0-3/HP` as the same thing; explicitly distinguish dipstick blood from microscopic RBC count.
- Do not ask the user to resend reports before searching accessible prior sources when they specifically say it was in prior/OpenClaw history.
- Do not save personal lab values in skills; use references for reusable search/recovery patterns, not patient-specific records.
