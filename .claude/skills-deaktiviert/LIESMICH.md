# Deaktivierte Skills

Hier liegen Skills, die Claude nicht mehr lädt, weil sie sich mit einem aktiven Skill überschneiden. Der Ordner heißt bewusst nicht `skills`, deshalb wird er beim Start nicht eingelesen.

Nichts wurde gelöscht. Zum Reaktivieren einfach zurückschieben:

```
mv .claude/skills-deaktiviert/frontend-design .claude/skills/
```

## Stand 17.08.2026

`frontend-design` und `huashu-design` wurden deaktiviert, weil `impeccable` als Design-Standard gilt (global installiert in `~/.claude/skills/impeccable`). Drei Design-Regelwerke nebeneinander führten dazu, dass Claude je nach Aufgabe ein anderes zieht.

`huashu-design` ist nur ein Symlink. Das Original liegt unverändert in `.agents/skills/huashu-design`.
