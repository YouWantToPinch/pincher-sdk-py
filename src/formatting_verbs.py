"""
The following types exist to provide this client with a means
of easily interpolating arguments into URL path parameters.

It is made to work like Go's formatting verbs.

Support only exists for strings.
For now, interpStringVerbs expects operands in variadic form,
for ease writing. This may need to change, however, as variadics
may wrongfully suggest that the operands are optional altogether,
which is NOT THE CASE.

To avoid throwing errors, calling interp_str_verbs DEMANDS an
operand for EVERY instance of '%s' within the original string.
"""

from typing import Any

S_VERB = "%s"


def interp_str_verbs(original: str, *args: Any) -> str:
    if len(args) == 0:
        raise ValueError("no operands provided for interpolation")
    formatted = original
    for i in range(len(args)):
        if S_VERB not in formatted:
            term = "arg" if i == 1 else "args"
            raise ValueError(
                f"inter_str_verbs format %s reads arg #{i + 1}, but call has {i} {term}"
            )
        formatted = formatted.replace(S_VERB, str(args[i]), count=1)

    return formatted
