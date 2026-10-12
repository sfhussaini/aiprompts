# Output Template: Image Prompt JSON

The final output must be a single JSON object following this structure:

```json
{
  "postive_prompt": "<[Subject/Character] is [Primary Action] with [Facial expressions] and [Body posture]. Dressed in [Clothing Detail], they reveal [Revealed Body Part(s)] while keeping [Covered Body Part(s) / Clothing Detail] covered. The scene takes place in [Scene/Environment Context], captured as a [Camera] shot with [Visual Style & Quality Modifiers]. [Dialogues] are shown as callouts over [Subject/Character].>",
  "negative_prompt": "<A comma-separated list of undesirable elements, e.g., (deformed, distorted, low quality, extra limbs)>",
  "wh_ratio": "<Aspect ratio, e.g., 3:2 or 2:3>"
}