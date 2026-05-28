# Week 5 Labs — AI APIs

Get base URL from stack output `ApiEndpoint`.

```bash
API=https://xxxx.execute-api.us-east-1.amazonaws.com/prod

curl -sS -X POST "$API/classify" -H "Content-Type: application/json" \
  -d '{"text":"Database replication lag in production"}' | jq .

curl -sS -X POST "$API/summarize" -H "Content-Type: application/json" \
  -d '{"text":"Pod crash loop after node upgrade. Errors in kubelet logs."}' | jq .

curl -sS -X POST "$API/route" -H "Content-Type: application/json" \
  -d '{"text":"Refund for cancelled subscription","label":"billing"}' | jq .
```

## Lab 5.2 — Cost controls

```bash
# Should return 400 input_too_large
python3 -c "print('{\"text\":\"" + 'x'*9000 + "\"}')" > /tmp/big.json
curl -sS -X POST "$API/classify" -H "Content-Type: application/json" -d @/tmp/big.json | jq .
```
