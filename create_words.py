words = [
    "code", "wire", "team", "base", "spy", "war", "peace", "navy",
    "army", "camp", "flag", "rank", "duty", "plan", "trap", "task",
    "work", "help", "mode", "sign", "data", "test", "file", "sort",
    "mark", "seek", "find", "safe", "lock", "send", "stop", "ship",
    "boat", "raid", "spot", "move", "form", "type", "scan", "grid",
    "radio", "tower", "field", "squad", "staff", "guard", "watch", "alert",
    "brain", "solve", "logic", "truth", "proof", "match", "track", "shift",
    "break", "crack", "force", "power", "speed", "smart", "quick", "vital",
    "wheel", "rotor", "cable", "panel", "board", "light", "sound", "relay",
    "morse", "phone", "voice", "click", "pulse", "swing", "pivot", "burst",
    "signal", "cipher", "secret", "combat", "attack", "defend", "strike", "target",
    "decode", "encode", "detect", "intercept", "transmit", "command", "mission", "beacon",
    "operate", "pattern", "network", "sequence", "machine", "complex", "urgent", "secure",
    "message", "station", "victory", "captain", "soldier", "officer", "general", "bureau",
    "support", "service", "connect", "transfer", "decrypt", "compute", "storage", "verify"
]

with open("words.txt", "w") as f:
    f.write("\n".join(words))

print(f"Created word list with {len(words)} words")
