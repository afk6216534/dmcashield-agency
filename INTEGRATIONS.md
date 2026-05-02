# DMCAShield Integrations Setup

## Email Integration (Resend)
- Provider: Resend.com
- API Key: Get from https://resend.com/api-keys
- Setup: Add RESEND_API_KEY to environment variables
- Usage: Used for email campaigns and outreach

## SMS Integration (Twilio)
- Provider: Twilio
- Account SID: Get from Twilio Console
- Auth Token: Get from Twilio Console  
- Phone Number: Get from Twilio Console
- Setup: Add to environment variables

## WhatsApp Integration (Twilio)
- Provider: Twilio (WhatsApp)
- Same credentials as SMS
- Enable WhatsApp in Twilio console

## OpenAI Integration
- Provider: OpenAI or compatible (OpenRouter)
- API Key: Get from https://openrouter.ai/keys
- Used for:
  - AIResponseHandler - Auto-generate responses
  - SelfLearning - Learn from interactions
  - Campaign content generation
- Setup: Add OPENAI_API_KEY or OPENROUTER_API_KEY

## Integration Status
```python
# In Settings page, enter:
- RESEND_API_KEY (for email)
- TWILIO_ACCOUNT_SID (for SMS/WhatsApp)
- TWILIO_AUTH_TOKEN
- TWILIO_PHONE_NUMBER
- OPENAI_API_KEY or OPENROUTER_API_KEY (for AI)
```

## Already Configured Endpoints
- /api/integrations - Check and manage integrations
- /api/email - Send emails
- /api/sms - Send SMS
- /api/whatsapp - Send WhatsApp