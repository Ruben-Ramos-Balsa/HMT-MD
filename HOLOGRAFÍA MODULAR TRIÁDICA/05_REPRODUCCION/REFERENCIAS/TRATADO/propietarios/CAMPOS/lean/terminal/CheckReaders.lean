import TerminalInputs

/-!
Diagnostic export for comparison with the original Python reader atlas.
This is not an additional HMT theorem and does not enumerate terminal states.
-/

open HMT.I.TerminalSelector

def main : IO Unit := do
  let times := n69Input.toList.map N69Row.time
  IO.println s!"META,{n69Input.size},{n69Input.all validN69Row},{times.eraseDups.length == times.length}"
  for row in n69Input do
    IO.println s!"ROW,{row.time},{row.bands[0]!},{row.bands[1]!},{row.bands[2]!},{row.fields[0]!},{row.fields[1]!},{row.fields[2]!},{row.fields[3]!}"
  let atlas := makeAtlas n69Input
  for (key, mask) in atlas.toList do
    IO.println s!"PAIR,{key},{mask}"
