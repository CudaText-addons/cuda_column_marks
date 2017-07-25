plugin for CudaText.
gives commands to work with vertical lines, "margins".
CudaText has 2 options:
- margin
- margin_string (numbers space-separated)

plugin reads all these margins, and gives commands:

- Set marks: prompts for additional margins on the fly, so no need
  to change option margin_string. can enter empty string to remove
  additional margins.
- Jump left: puts caret (needs single caret) on the lefter margin (or column 0).
- Jump right: puts caret on the righter margin.

author: Alexey (CudaText)
license: MIT
