<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Output Contract — code or schema reference

Paths and commands use the skill root as their context.

```json
{
  "$schema": "https://developers.openai.com/apps-sdk/schemas/chatgpt-app-submission.v1.json",
  "schema_version": 1,
  "app_info": {
    "display_name": "Example App",
    "subtitle": "Find and update records",
    "description": "Example App helps users find records, inspect details, and update workspace data through ChatGPT.",
    "category": "PRODUCTIVITY"
  },
  "tools": {
    "tool_name": {
      "annotations": {
        "readOnlyHint": true,
        "openWorldHint": false,
        "destructiveHint": false
      },
      "justifications": {
        "read_only_justification": "Only retrieves matching records and does not modify data.",
        "open_world_justification": "Does not write to public internet state or third-party systems.",
        "destructive_justification": "Does not delete, overwrite, revoke access, or perform irreversible actions."
      }
    }
  },
  "test_cases": [
    {
      "description": "Find records that match a specific user request.",
      "user_prompt": "Find my open records for this week.",
      "file_attachment_urls": null,
      "tools_triggered": "tool_name",
      "expected_output": "Returns matching records with enough detail for the user to choose the next action.",
      "expected_output_url": null
    }
  ],
  "negative_test_cases": [
    {
      "description": "Do not trigger for unrelated calendar requests.",
      "user_prompt": "What meetings do I have tomorrow?",
      "file_attachment_urls": null,
      "tools_triggered": null,
      "expected_output": "The app should not be invoked because the request is outside its supported workflows.",
      "expected_output_url": null
    }
  ]
}
```
