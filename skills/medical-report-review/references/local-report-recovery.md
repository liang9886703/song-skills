# Local Report Recovery Checklist

Use when the user says a medical/inspection report was shared in prior OpenClaw/Hermes history but normal session search does not surface the values.

## Search targets

- Conversation history: `session_search` for domain terms and prior mentions.
- OpenClaw session logs: `~/.openclaw/agents/**/sessions/*.jsonl*`.
- Gateway/tool logs if present: `~/.openclaw/logs/`.
- Inbound media: `~/.openclaw/media/inbound/`.
- Extracted artifacts: `~/.openclaw/workspace/tmp/`, especially `report.txt`, `*.txt`, `*.md`, OCR outputs, or converted PDFs.

## Useful keyword sets

For hematuria/renal reports:

```text
尿常规|尿隐血|潜血|红细胞|尿红细胞|尿蛋白|白细胞|亚硝酸盐|管型|结晶
肾功能|肌酐|eGFR|尿素|尿素氮|尿酸|胱抑素
彩超|双肾|输尿管|膀胱|前列腺|肾囊肿|积水
```

For report files generally:

```text
体检|报告|检查|检验|化验|医院|检测机构|采集时间|报告时间
```

## Practical pattern

1. Locate candidate extracted text or report media.
2. Keyword-search the extracted text, then read 30-80 lines around matches instead of dumping the full report.
3. Preserve result metadata: date, test section, value, unit, reference range, abnormal flag.
4. Summarize only relevant findings and normal negatives.
5. State what prior findings make less likely, then what the current symptom still requires rechecking.

## Safety/privacy

- Do not paste signed/private URLs from logs.
- Do not expose unrelated report sections.
- Do not store patient-specific values in this reference; keep the pattern reusable.
