# Groq Whisper setup guide

## Features
When a YouTube/Bilibili video has no subtitles, use Groq's Whisper API to transcribe
the audio. Groq provides a free usage allowance.

## Steps the agent can complete automatically

1. Check whether it is configured:
```bash
agent-reach doctor | grep -i "groq\|whisper"
```

2. If the user provides a key, save it in the configuration:
```python
from agent_reach.config import Config
c = Config()
c.set("groq_api_key", "USER_PROVIDED_KEY")
```

3. Test (optional):
```bash
curl -s https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer USER_PROVIDED_KEY" \
  -o /dev/null -w "%{http_code}"
```
A 200 response means the API is available.

## Steps the user must complete manually

Tell the user:

> Video transcription requires a Groq API key (free).
>
> Steps:
> 1. Open https://console.groq.com
> 2. Sign up with Google or an email address
> 3. Click "API Keys" on the left
> 4. Click "Create API Key"
> 5. Copy the generated key and send it to me
>
> Groq offers a free usage allowance that is sufficient for everyday use.

## What the agent does after receiving the key

1. Save it in the configuration: `config.set("groq_api_key", key)`
2. Test API availability
3. Report: "✅ Transcription is enabled! I can now extract content from videos even when they have no subtitles."
