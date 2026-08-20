"""A small offline list of very common passwords, used to flag obviously weak choices.

This is a short educational sample, not an exhaustive breach database. The
checker never sends the password anywhere, it only compares it locally
against this list.
"""

COMMON_PASSWORDS = {
    "123456", "password", "123456789", "12345678", "12345", "qwerty",
    "abc123", "111111", "123123", "1234567", "password1", "iloveyou",
    "adobe123", "qwerty123", "letmein", "monkey", "sunshine", "welcome",
    "admin", "login", "princess", "solo", "starwars", "football",
    "dragon", "master", "hello", "freedom", "whatever", "trustno1",
    "000000", "1q2w3e4r", "qazwsx", "michael", "jennifer", "jordan23",
    "superman", "batman", "121212", "flower", "hottie", "loveme",
    "zaq1zaq1", "password123", "1234", "12345678910", "asdfghjkl",
    "changeme", "passw0rd", "1qaz2wsx", "azerty", "motdepasse",
    "bonjour", "soleil", "chocolat", "marseille",
}
