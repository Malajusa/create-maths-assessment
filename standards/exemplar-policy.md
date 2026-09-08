# Exemplar Policy

Exemplars are authoritative only for the dimensions explicitly assigned to them.

Possible roles include:
- visual layout;
- typography;
- question density;
- working-space expectations;
- problem quality;
- complexity;
- diagram style;
- marking-key presentation.

## Precedence

1. Explicit current user instruction
2. Current canonical standards
3. Current curriculum requirements
4. Assigned exemplar characteristics
5. Older examples and historical outputs

Do not copy an exemplar's outdated curriculum claim, mathematical error or superseded rule merely because its visual form is preferred.

## Extraction

Before generation, extract an `exemplar_profile` describing only the relevant reusable characteristics. Downstream agents should consume that profile rather than repeatedly reinterpreting the source.

## Alternate versions

When the user requests a Version B/practice version:
- preserve the intended skills, marks and difficulty;
- change values and associated visuals consistently;
- change contexts where requested;
- re-solve every changed question;
- do not let superficial number substitution introduce different mathematical difficulty.
